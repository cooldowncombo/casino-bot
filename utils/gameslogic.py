import discord
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

def format_credits(amount: int) -> str:
    """Format credits with commas and proper pluralization"""
    formatted = f"{amount:,}"
    if amount == 1:
        return f"{formatted} credit"
    else:
        return f"{formatted} credits"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a percentage value"""
    return f"{value:.{decimals}f}%"

def format_multiplier(value: float) -> str:
    """Format a multiplier value"""
    return f"{value:.1f}x"

def calculate_house_edge(total_wagered: int, total_payout: int) -> float:
    """Calculate house edge percentage"""
    if total_wagered == 0:
        return 0.0
    return ((total_wagered - total_payout) / total_wagered) * 100

def is_valid_bet(bet: int, min_bet: int = 1, max_bet: int = 10000) -> tuple[bool, str]:
    """Validate a bet amount"""
    if bet < min_bet:
        return False, f"Minimum bet is {format_credits(min_bet)}"
    if bet > max_bet:
        return False, f"Maximum bet is {format_credits(max_bet)}"
    return True, ""

def get_win_streak_emoji(streak: int) -> str:
    """Get emoji for win streak"""
    if streak >= 10:
        return "🔥🔥🔥"
    elif streak >= 5:
        return "🔥🔥"
    elif streak >= 3:
        return "🔥"
    else:
        return ""

def get_rank_emoji(rank: int) -> str:
    """Get emoji for leaderboard rank"""
    rank_emojis = {
        1: "🥇",
        2: "🥈", 
        3: "🥉"
    }
    return rank_emojis.get(rank, "🏆")

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{hours}h"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, return default if denominator is 0"""
    if denominator == 0:
        return default
    return numerator / denominator

def parse_json_safely(json_string: str, default: Dict[str, Any] = None) -> Dict[str, Any]:
    """Safely parse JSON string, return default if parsing fails"""
    if default is None:
        default = {}
    if not json_string:
        return default
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default

def get_time_until_next_daily() -> Optional[timedelta]:
    """Calculate time until next daily bonus (placeholder - would need user data)"""
    # This would need to be implemented with actual user data
    # For now, return None
    return None

def format_timeframe(hours: int) -> str:
    """Format timeframe for statistics"""
    if hours == 1:
        return "Last Hour"
    elif hours == 24:
        return "Last 24 Hours"
    elif hours == 168:  # 7 days
        return "Last Week"
    elif hours == 720:  # 30 days
        return "Last Month"
    else:
        return f"Last {hours} Hours"

def get_game_icon(game_type: str) -> str:
    """Get emoji icon for game type"""
    icons = {
        'slots': '🎰',
        'blackjack': '🃏',
        'roulette': '🎯',
        'coinflip': '🪙',
        'dice': '🎲',
        'crash': '📈',
        'mines': '💣'
    }
    return icons.get(game_type.lower(), '🎮')

def calculate_rtp(total_wagered: int, total_payout: int) -> float:
    """Calculate Return to Player percentage"""
    if total_wagered == 0:
        return 0.0
    return (total_payout / total_wagered) * 100

def get_profit_color(profit: int) -> discord.Color:
    """Get color based on profit/loss"""
    if profit > 0:
        return discord.Color.green()
    elif profit < 0:
        return discord.Color.red()
    else:
        return discord.Color.gold()

def chunk_list(lst: list, chunk_size: int) -> list:
    """Chunk a list into smaller lists of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def get_level_from_experience(experience: int) -> int:
    """Calculate player level from total experience/games played"""
    # Simple level calculation - could be made more complex
    if experience < 10:
        return 1
    elif experience < 50:
        return 2
    elif experience < 150:
        return 3
    elif experience < 300:
        return 4
    elif experience < 500:
        return 5
    else:
        return min(10, 5 + (experience - 500) // 200)

def get_level_emoji(level: int) -> str:
    """Get emoji for player level"""
    if level >= 10:
        return "🌟"
    elif level >= 7:
        return "⭐"
    elif level >= 5:
        return "✨"
    elif level >= 3:
        return "🔸"
    else:
        return "🔹"

class CooldownManager:
    """Simple cooldown manager for commands"""
    def __init__(self):
        self.cooldowns = {}

    def is_on_cooldown(self, user_id: int, command: str, cooldown_seconds: int) -> bool:
        """Check if user is on cooldown for a command"""
        key = f"{user_id}:{command}"
        if key not in self.cooldowns:
            return False
        time_since = (datetime.utcnow() - self.cooldowns[key]).total_seconds()
        return time_since < cooldown_seconds

    def add_cooldown(self, user_id: int, command: str):
        """Add cooldown for user and command"""
        key = f"{user_id}:{command}"
        self.cooldowns[key] = datetime.utcnow()

    def get_remaining_cooldown(self, user_id: int, command: str, cooldown_seconds: int) -> int:
        """Get remaining cooldown time in seconds"""
        key = f"{user_id}:{command}"
        if key not in self.cooldowns:
            return 0
        time_since = (datetime.utcnow() - self.cooldowns[key]).total_seconds()
        remaining = cooldown_seconds - time_since
        return max(0, int(remaining))

# Global cooldown manager instance
cooldown_manager = CooldownManager()