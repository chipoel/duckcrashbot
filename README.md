# Crash Game Betting Bot

This project implements a betting bot for a crash game using the Martingale strategy. The bot places orders based on the game results and adjusts the bet size accordingly. The bot supports multiple accounts and uses the game API to place bets and check results.

## Features

- **Martingale Strategy**: Increases the bet size after a loss to recover previous losses and gain a profit.
- **Multiple Accounts**: Supports betting for multiple accounts simultaneously.
- **Automated Betting**: Automatically places bets based on the game results and account balance.
- **Configurable Parameters**: Allows setting initial bet size and balance thresholds.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crash-game-betting-bot.git
   cd crash-game-betting-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install requests
   ```

## Configuration

Update the `authorization_tokens` list in the `run.py` script with your own authorization tokens:

```python
authorization_tokens = [
    "Bearer your_first_token",
    "Bearer your_second_token"
]
```

## Usage

Run the bot:

```bash
python run.py
```

The bot will run in a loop, checking the balance and placing bets every 15 seconds. It will adjust the bet size based on the results of the previous game using the Martingale strategy.

## Strategy

1. **Initial Bet Size**: The bot starts with an initial bet size of 500.
2. **Increase Bet Size on Loss**: If the previous bet is lost (i.e., the game result is below 1.1), the bot increases the bet size to 5000 for the next bet.
3. **Reset Bet Size on Win**: If the previous bet is won (i.e., the game result is 1.1 or higher), the bot resets the bet size to 500.
4. **Balance Check**: The bot will only place bets if the balance is above a threshold (10,000).

### Recommended Starting Balance

For optimal performance and to handle potential losses, it is recommended to start with a balance of at least 16,500 Ducks.

## Project Structure

- `run.py`: The main script that implements the betting logic and Martingale strategy.
- `README.md`: This file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests.

## Disclaimer

This project is for educational purposes only. Use it at your own risk. The author is not responsible for any financial losses or damages that may occur as a result of using this bot.
