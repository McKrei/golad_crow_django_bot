
from bot.main import bot


async def send_messages(reports):
    for report in reports.reports:
        await bot.send_message(
            report.id,
            report.message)
