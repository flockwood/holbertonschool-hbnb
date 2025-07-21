#!/usr/bin/env python3
"""
Master test runner for all HBnB tests.
"""

import sys
import os
import subprocess

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_file(test_file, description):
    """Run a specific test file."""
    print(f"\n{'='*60}")
    print(f"🧪 Running {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 HBnB MASTER TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("tests/quick_system_check.py", "Quick System Health Check"),
        ("tests/comprehensive_test_suite.py", "Comprehensive System Test"),
        ("tests/test_jwt_auth.py", "JWT Authentication Test"),
        ("tests/test_password_hashing.py", "Password Hashing Test"),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        if os.path.exists(test_file):
            if run_test_file(test_file, description):
                passed += 1
        else:
            print(f"⚠️  Test file not found: {test_file}")
    
    print(f"\n{'='*60}")
    print(f"📊 MASTER TEST RESULTS: {passed}/{total} test suites passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 ALL TEST SUITES PASSED!")
    else:
        print("⚠️  Some test suites had issues. Check output above.")

if __name__ == "__main__":
    main()
