import requests
import subprocess
from urllib.parse import urlparse
import logging
from typing import Tuple, Optional
import json


class ConnectivityChecker:
    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('connectivity_checker')
        if not logger.handlers:
            # 添加控制台处理器 - 使用简单格式
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

            # 添加文件处理器 - 使用详细格式
            file_handler = logging.FileHandler('connectivity_check.log')
            # 修改格式化器，使用条件格式
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s\n'
                '%(details)s\n'
                '----------------------------------------',
                defaults={'details': 'No additional details'}  # 提供默认值
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            logger.setLevel(logging.INFO)
        return logger

    def _log_command(self, command: str, output: str, level: str = "info", **kwargs):
        """统一的命令日志记录函数"""
        details = f"Command: {command}\nOutput: {output}"
        if level == "error":
            self.logger.error(command, extra={'details': details})
        else:
            self.logger.info(command, extra={'details': details})

    def _log_step(self, message: str, details: str = None):
        """记录普通步骤信息"""
        self.logger.info(
            message, extra={'details': details or "Step information"})

    def check_http_status(self) -> Tuple[bool, str]:
        self._log_step(f"开始检查 HTTP 状态: {self.url}")
        try:
            response = requests.get(self.url, timeout=10)
            output = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'elapsed': str(response.elapsed)
            }
            self._log_command(
                command=f"GET {self.url}",
                output=json.dumps(output, indent=2)
            )

            if response.status_code == 200:
                return True, "HTTP Status 200: OK"
            else:
                return False, f"HTTP Error: Status Code {response.status_code}"
        except Exception as e:
            self._log_command(
                command=f"GET {self.url}",
                output=str(e),
                level="error"
            )
            return False, str(e)

    def check_dns(self) -> Tuple[bool, str]:
        command = ["nslookup", self.domain]
        self._log_step(f"开始 DNS 检查: {self.domain}")
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )
            self._log_command(
                command=' '.join(command),
                output=result.stdout + result.stderr
            )

            if "can't find" in result.stdout or "NXDOMAIN" in result.stdout:
                return False, "DNS Lookup failed"
            return True, "DNS Lookup successful"
        except Exception as e:
            self._log_command(
                command=' '.join(command),
                output=str(e),
                level="error"
            )
            return False, str(e)

    def check_ping(self) -> Tuple[bool, str]:
        command = ["ping", "-c", "1", self.domain]
        self.logger.info(f"开始 Ping 检查: {self.domain}")
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )
            self._log_command(
                command=' '.join(command),
                output=result.stdout + result.stderr
            )

            if "1 packets transmitted, 1" in result.stdout and "0% packet loss" in result.stdout:
                return True, "Ping successful"
            return False, "Ping failed"
        except Exception as e:
            self._log_command(
                command=' '.join(command),
                output=str(e),
                level="error"
            )
            return False, str(e)

    def check_port(self, port: Optional[int] = None) -> Tuple[bool, str]:
        if port is None:
            port = 443 if self.url.startswith("https") else 80

        command = ["nc", "-zv", "-w", "5", self.domain, str(port)]
        self.logger.info(f"开始端口检查: {self.domain}:{port}")
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )
            self._log_command(
                command=' '.join(command),
                output=result.stdout + result.stderr
            )

            if result.returncode == 0:
                return True, f"Port {port} is open"
            return False, f"Port {port} is closed"
        except Exception as e:
            self._log_command(
                command=' '.join(command),
                output=str(e),
                level="error"
            )
            return False, str(e)

    def check_ssl_certificate(self) -> Tuple[bool, str]:
        if not self.url.startswith("https"):
            return True, "Not an HTTPS URL, skipping SSL check"

        command = ["openssl", "s_client", "-connect", f"{self.domain}:443",
                   "-servername", self.domain]
        self.logger.info(f"开始 SSL 证书检查: {self.domain}")
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input="Q\n")

            self._log_command(
                command=' '.join(command),
                output=f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
            )

            if "Verify return code: 0 (ok)" in stderr:
                return True, "SSL Certificate is valid"
            return False, "SSL Certificate is invalid"
        except Exception as e:
            self._log_command(
                command=' '.join(command),
                output=str(e),
                level="error"
            )
            return False, str(e)

    def analyze_connectivity(self) -> dict:
        self._log_step(
            f"开始全面连通性分析: {self.url}",
            "Starting comprehensive connectivity analysis"
        )
        results = {}

        # 1. Check HTTP Status
        status, message = self.check_http_status()
        results["http_status"] = {"success": status, "message": message}

        # 2. Check DNS
        status, message = self.check_dns()
        results["dns"] = {"success": status, "message": message}

        # 3. Check Ping
        status, message = self.check_ping()
        results["ping"] = {"success": status, "message": message}

        # 4. Check Port
        status, message = self.check_port()
        results["port"] = {"success": status, "message": message}

        # 5. Check SSL (if HTTPS)
        if self.url.startswith("https"):
            status, message = self.check_ssl_certificate()
            results["ssl"] = {"success": status, "message": message}

        self._log_step(
            f"连通性分析完成",
            f"Analysis results:\n{json.dumps(results, indent=2, ensure_ascii=False)}"
        )
        return results
