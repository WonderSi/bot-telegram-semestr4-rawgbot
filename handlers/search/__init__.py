from aiogram import Router
from handlers.search.command import router as command_router
from handlers.search.callbacks import router as callbacks_router
from handlers.search.states import router as states_router
from handlers.search.navigation import router as navigation_router

router = Router()
router.include_router(command_router)
router.include_router(callbacks_router)
router.include_router(states_router)
router.include_router(navigation_router)

__all__ = ['router']
