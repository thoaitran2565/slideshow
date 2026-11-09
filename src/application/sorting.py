import re
from typing import List, Union


def natural_sort_key(s: str) -> List[Union[int, str]]:
    """
    Hỗ trợ sắp xếp chuỗi theo chuẩn số tự nhiên của Windows File Explorer.
    Ví dụ: '2.jpg' sẽ đứng trước '10.jpg'.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

