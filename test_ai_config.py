#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test kết nối AI Assistant
Chạy trực tiếp để kiểm tra cấu hình mà không cần Odoo GUI
"""

import os
import json
import requests
import sys
from pathlib import Path

# Màu cho terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_status(status, message):
    """In trạng thái với màu"""
    if status == "success":
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}✗ {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")
    else:
        print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def test_openrouter(api_key):
    """Test kết nối OpenRouter API"""
    print(f"\n{Colors.BOLD}Testing OpenRouter API...{Colors.END}")
    
    if not api_key or api_key == "sk-or-v1-default-test-key":
        print_status("warning", "API Key là giá trị mặc định. Vui lòng nhập API Key thật từ https://openrouter.ai")
        return False
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:8069",
        "X-Title": "Odoo FitDNU"
    }
    
    payload = {
        "model": "xiaomi/mimo-v2-flash:free",
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý AI hữu ích."},
            {"role": "user", "content": "Xin chào, bạn là ai?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print_status("info", "Gửi request đến OpenRouter API...")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0]["message"]["content"]
                print_status("success", f"Kết nối thành công!")
                print(f"  Phản hồi: {message[:100]}...")
                return True
            else:
                print_status("error", f"Response không có choices")
                print(f"  {result}")
                return False
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            print_status("error", f"HTTP {response.status_code}: {error_msg}")
            return False
            
    except requests.exceptions.Timeout:
        print_status("error", "Request timeout. Kiểm tra kết nối internet.")
        return False
    except requests.exceptions.ConnectionError:
        print_status("error", "Không thể kết nối đến server. Kiểm tra internet.")
        return False
    except Exception as e:
        print_status("error", f"Lỗi: {str(e)}")
        return False

def test_openai(api_key):
    """Test kết nối OpenAI API"""
    print(f"\n{Colors.BOLD}Testing OpenAI API...{Colors.END}")
    
    if not api_key or api_key.startswith("sk-"):
        print_status("warning", "Hãy nhập OpenAI API Key thật")
        return False
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hi, who are you?"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print_status("success", "Kết nối OpenAI thành công!")
            return True
        else:
            print_status("error", f"OpenAI error: {response.status_code}")
            return False
    except Exception as e:
        print_status("error", f"OpenAI connection failed: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== AI Assistant Cấu hình Test ==={Colors.END}\n")
    
    # 1. Kiểm tra file cấu hình
    print_status("info", "Kiểm tra cấu hình hệ thống...")
    
    # 2. Đọc API Key từ input
    print(f"\n{Colors.BOLD}Nhập API Key để test:{Colors.END}")
    print("1. OpenRouter (khuyến nghị): sk-or-v1-xxxxx")
    print("2. OpenAI: sk-xxxxx")
    print("3. Bỏ qua: Nhấn Enter\n")
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print_status("warning", "Chưa nhập API Key. Sử dụng giá trị mặc định.")
        api_key = None
    
    # 3. Tự động phát hiện loại API
    if api_key:
        if api_key.startswith("sk-or"):
            test_openrouter(api_key)
        elif api_key.startswith("sk-"):
            test_openai(api_key)
        else:
            print_status("warning", "Không nhận dạng được loại API Key")
    
    # 4. Gợi ý tiếp theo
    print(f"\n{Colors.BOLD}Bước tiếp theo:{Colors.END}")
    print("1. Vào Odoo: http://localhost:8069")
    print("2. Menu: AI Assistant > Cấu hình")
    print("3. Nhập API Key và các thông tin cấu hình")
    print("4. Nhấn 'Test kết nối' để xác nhận")
    print("5. Lưu cấu hình")
    
    print(f"\n{Colors.GREEN}✓ Test hoàn tất!{Colors.END}\n")

if __name__ == "__main__":
    main()
