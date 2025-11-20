# Nautifier

A simple GitHub Actions-powered bot that fetches the daily USD to CNY exchange rate and sends it to a Telegram chat.

## Features

- Fetches exchange rates from [ExchangeRate-API](https://www.exchangerate-api.com/).
- Sends a formatted message to a specified Telegram chat.
- Runs automatically every day at 00:00 UTC (8:00 AM Beijing Time).
- Can be triggered manually via GitHub Actions.

## Setup

### Prerequisites

1.  **Telegram Bot**: Create a bot using [BotFather](https://t.me/BotFather) and get the `API Token`.
2.  **Chat ID**: Get the Chat ID where you want to receive messages (you can use `@userinfobot` or similar tools).

### GitHub Secrets Configuration

To make the workflow run, you need to add the following secrets to your GitHub repository:

1.  Go to your repository on GitHub.
2.  Navigate to **Settings** > **Secrets and variables** > **Actions**.
3.  Click **New repository secret**.
4.  Add the following secrets:
    *   `TELEGRAM_BOT_TOKEN`: Your Telegram Bot API Token.
    *   `TELEGRAM_CHAT_ID`: The Chat ID where messages should be sent.
    *   `RAPIDAPI_KEY`: Your RapidAPI Key for Yahoo Finance (optional, for stock prices).

## Usage

The workflow is configured to run automatically. To run it manually:

1.  Go to the **Actions** tab in your repository.
2.  Select **Daily Exchange Rate Notification** from the left sidebar.
3.  Click **Run workflow**.
