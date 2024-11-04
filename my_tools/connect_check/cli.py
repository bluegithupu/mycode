import argparse
import json
from .checker import ConnectivityChecker
from .analyzer import ConnectivityAnalyzer
import os

def main():
    parser = argparse.ArgumentParser(
        description='Check connectivity of HTTP/HTTPS endpoints'
    )
    parser.add_argument('url', help='URL to check (e.g., https://example.com)')
    parser.add_argument(
        '--analyze', 
        action='store_true',
        help='Perform AI analysis of the results'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'html'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    args = parser.parse_args()
    
    # 执行连通性检查
    checker = ConnectivityChecker(args.url)
    check_results = checker.analyze_connectivity()
    
    # 准备完整的结果数据
    results = {
        "url": args.url,
        "checks": check_results
    }
    
    if args.analyze:
        try:
            # 执行 AI 分析
            analyzer = ConnectivityAnalyzer()
            analysis = analyzer.analyze_report(results)
            
            if "error" in analysis:
                print(f"\nAI Analysis failed: {analysis['error']}")
                print_basic_results(args.url, check_results, args.format)
                return
                
            results["analysis"] = analysis
            
            # 生成报告
            if args.format == 'json':
                print(json.dumps(results, indent=2, ensure_ascii=False))
            else:
                report = analyzer.generate_report(results, analysis, args.format)
                print("\n" + report)
                
        except Exception as e:
            print(f"\nAI Analysis failed: {str(e)}")
            print_basic_results(args.url, check_results, args.format)
    else:
        print_basic_results(args.url, check_results, args.format)

def print_basic_results(url: str, check_results: dict, format: str = 'markdown'):
    """打印基本检查结果"""
    if format == 'json':
        print(json.dumps({"url": url, "checks": check_results}, indent=2))
        return
        
    print(f"\nConnectivity Check Results for {url}\n")
    print("-" * 50)
    for check_name, result in check_results.items():
        status = "✓" if result["success"] else "✗"
        print(f"{check_name.upper():12} [{status}] {result['message']}")
    print("-" * 50)

if __name__ == "__main__":
    main() 