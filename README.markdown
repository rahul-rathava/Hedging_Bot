# Spot Exposure Hedging Bot

   ## Overview
   A Python-based bot to monitor and hedge spot position risks using Bybit perpetual futures, controlled via Telegram.

   ## Setup
   1. Install Python 3.8+ and libraries: `pip install -r requirements.txt`.
   2. Get Bybit API key from [Bybit](https://www.bybit.com).
   3. Get Telegram bot token from @BotFather.
   4. Update `bot_hedging.py` with your API token.

   ## Risk Calculation
   - **Delta**: Position size (e.g., 1 BTC = delta 1).
   - **Hedge Ratio**: Spot delta / futures contract size (0.001 BTC).
   - Formula: `hedge_ratio = spot_delta / 0.001`.

   ## Bot Commands
   - `/monitor_risk <asset> <size> <threshold>`: Start monitoring (e.g., `/monitor_risk BTC 1.0 0.5`).
   - Inline button “Hedge Now”: Triggers hedging action.

   ##  Features
   | Feature | Description |
   |--------|-------------|
   | /start | Welcome message |
   | /monitor_risk `<asset>` `<size>` `<threshold>` | Calculates risk exposure |
   | /hedge_now | Simulates hedge with calculated size |
   | /hedge_status | Shows current hedge setup |
   | /hedge_history | Shows all previous hedge actions |
   | /hedge_chart | Sends bar chart of hedge sizes |
   | /auto_hedge on/off | Auto-hedging toggle for 24x7 risk control |

   ##  Sample Interaction
   ```
   /monitor_risk BTC 1.5 0.3
    High risk for BTC!
    Suggested Hedge: 1.42 BTC

   /hedge_now
    Simulated hedge executed for 1.42 BTC

   /hedge_chart
   [ Bar chart image]

   /auto_hedge on
    Auto-Hedging Enabled
   ```

   ## Limitations
   - Supports only Bybit and BTC/USDT for demo.
   - Simplified delta calculation; no gamma/theta/vega.
   - No real trades (simulated for demo).

   ## Deployment
   Run `python bot_hedging.py` and interact via Telegram.
