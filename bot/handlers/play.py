"""Module for play in the bot."""

from aiogram import F, Bot, types
from aiogram.fsm.context import FSMContext
from utils import get_auth_from_state
from utils.state import GameState
from handlers import router
from utils import (
    check_winner,
    get_game_keyboard,
    is_board_full,
    build_headers
)
import httpx


@router.callback_query(F.data.startswith("cell_"))
async def handle_move(
    callback_query: types.CallbackQuery,
    bot: Bot,
    state: FSMContext,
    api_url: str,
):
    """
    Process a player's move in an ongoing Tic-Tac-Toe game.

    Args:
        callback_query (types.CallbackQuery): Callback user's action.
        bot (Bot): Send messages and interact with the Telegram API.
        games (dict): A dictionary containing the current state of all games.
        api_url (str): A string representing api url.
    """
    games =  await state.get_data('games')
    user_id = callback_query.from_user.id
    game_id = next(
        (gid for gid, game in games.items() if user_id in game["players"]),
        None
    )
    if game_id is None:
        await callback_query.answer("Начните новую игру с /start")
        return
    board = games[game_id]["board"]
    turn = games[game_id]["turn"]
    opponent_id: int = next(
        pid for pid in games[game_id]["players"] if pid != user_id
    )
    username = games[game_id]["players"][user_id]["username"]

    if turn != games[game_id]["players"][opponent_id]["symbol"]:
        await callback_query.answer("Не ваш ход!")
        return

    if callback_query.data is None:
        return
    i, j = map(int, callback_query.data.split("_")[1:])
    if board[i][j] != " ":
        await callback_query.answer("Неверный ход! Эта клетка уже занята.")
        return

    if (
        isinstance(
            callback_query.message,
            types.InaccessibleMessage
        ) or callback_query.message is None
    ):
        return
    board[i][j] = turn
    winner = check_winner(board)
    if winner:
        if winner == "O":
            winner = games[game_id]['players'][opponent_id]['username']
        else:
            winner = games[game_id]['players'][user_id]['username']
        await callback_query.message.edit_text(
            f"Игра окончена! {winner} победил!", reply_markup=None
        )
        games.pop(game_id)
        await bot.send_message(
            opponent_id, f"Игра окончена! {winner} победил!", reply_markup=None
        )
        access_token = await get_auth_from_state(
            state,
            api_url,
            user_id,
            username
        )
        async with httpx.AsyncClient(
            base_url=api_url, headers=build_headers(access_token)
        ) as client:
            await client.post(
                "/games/",
                json={
                    "player1_id": user_id if turn == "X" else opponent_id,
                    "player2_id": opponent_id if turn == "X" else user_id,
                    "result": winner,
                },
            )
        return
    if is_board_full(board):
        await callback_query.message.edit_text(
            "Игра окончена! Ничья!", reply_markup=None
        )
        games.pop(game_id)
        await bot.send_message(
            opponent_id,
            "Игра окончена! Ничья!",
            reply_markup=None
        )
        access_token = await get_auth_from_state(
            state,
            api_url,
            user_id,
            username
        )
        async with httpx.AsyncClient(
            base_url=api_url, headers=build_headers(access_token)
        ) as client:
            await client.post(
                "/games/",
                json={
                    "player1_id": user_id,
                    "player2_id": opponent_id,
                    "result": "draw",
                },
            )
        return
    games[game_id]["turn"] = "O" if turn == "X" else "X"
    await state.update_data(games=games)
    await callback_query.message.edit_text(
        f"Ход {games[game_id]['players'][opponent_id]['username']}:",
        reply_markup=get_game_keyboard(board),
    )
    await bot.send_message(
        opponent_id, f"Ваш ход:", reply_markup=get_game_keyboard(board)
    )
    await callback_query.answer()
