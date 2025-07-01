from django import template

register = template.Library()

@register.filter
def force_intcomma(value):
    """
    数値を強制的に3桁カンマ区切りの文字列に変換するフィルタ。
    intcommaが期待通りに動かない場合に使用する。
    """
    try:
        # まずは値を整数に変換しようと試みる
        int_value = int(value)
        # formatを使ってカンマ区切り文字列に変換して返す
        return "{:,}".format(int_value)
    except (ValueError, TypeError):
        # もし数値に変換できない値が来たら、そのまま返す
        return value