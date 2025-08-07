#!/usr/bin/env python3
"""
Quality Assurance Framework - Automated security and quality checks
"""

import subprocess
import sys
import json
from pathlib import Path


class QualityGate:
    """Automated quality gate enforcement"""
    
    def __init__(self):
        self.results = {}
        self.passed = True
    
    def run_security_scan(self):
        """Run security vulnerability scan"""
        try:
            result = subprocess.run(['bandit', '-r', 'src/', '-f', 'json'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.results['security'] = 'FAIL'
                self.passed = False
            else:
                self.results['security'] = 'PASS'
        except FileNotFoundError:
            self.results['security'] = 'SKIP - bandit not installed'
    
    def run_regression_tests(self):
        """Run regression test suite"""
        try:
            result = subprocess.run(['python', '-m', 'pytest', 'tests/test_regression.py', '-v'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.results['regression'] = 'PASS'
            else:
                self.results['regression'] = 'FAIL'
                self.passed = False
        except FileNotFoundError:
            self.results['regression'] = 'SKIP - pytest not available'
    
    def validate_security_fixes(self):
        """Validate critical security fixes"""
        try:
            # Test path traversal protection
            from dmps.security import SecurityConfig
            if SecurityConfig.is_safe_path("../../../etc/passwd"):
                self.results['path_traversal'] = 'FAIL - Path traversal not blocked'
                self.passed = False
            else:
                self.results['path_traversal'] = 'PASS'
            
            # Test input validation
            from dmps.validation import InputValidator
            validator = InputValidator()
            result = validator.validate_input("<script>alert('xss')</script>test")
            if not result.warnings:
                self.results['input_validation'] = 'FAIL - XSS not detected'
                self.passed = False
            else:
                self.results['input_validation'] = 'PASS'
                
        except Exception as e:
            self.results['validation'] = f'ERROR - {str(e)}'
            self.passed = False
    
    def check_performance_optimizations(self):
        """Verify performance optimizations are in place"""
        try:
            from dmps.techniques import OptimizationTechniques
            tech = OptimizationTechniques()
            
            # Check compiled patterns exist
            if not hasattr(tech, '_CONTEXT_PATTERN'):
                self.results['performance'] = 'FAIL - Compiled patterns missing'
                self.passed = False
            else:
                self.results['performance'] = 'PASS'
        except Exception as e:
            self.results['performance'] = f'ERROR - {str(e)}'
            self.passed = False
    
    def generate_report(self):
        """Generate quality gate report"""
        print("=" * 60)
        print("QUALITY GATE REPORT")
        print("=" * 60)
        
        for check, result in self.results.items():
            status = "✅" if result == 'PASS' else "❌" if 'FAIL' in result else "⚠️"
            print(f"{status} {check.upper()}: {result}")
        
        print("=" * 60)
        if self.passed:
            print("🎉 ALL QUALITY GATES PASSED")
            return 0
        else:
            print("🚨 QUALITY GATE FAILURES DETECTED")
            return 1
    
    def run_all(self):
        """Run all quality checks"""
        print("Running Quality Assurance Framework...")
        
        self.run_security_scan()
        self.run_regression_tests()
        self.validate_security_fixes()
        self.check_performance_optimizations()
        
        return self.generate_report()


def main():
    """Main entry point"""
    gate = QualityGate()
    exit_code = gate.run_all()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()