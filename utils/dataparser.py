# -*- coding: utf-8 -*-
import configparser
import json
import os

from PyQt5.QtWidgets import QMessageBox


class ConfigManager:
    def __init__(self, config_path='config.ini'):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Load the configuration file."""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path, encoding='utf-8')

    def save_config(self):
        """Save the configuration file."""
        try:
            with open('config.ini', 'w', encoding="utf-8") as config_file:
                self.config.write(config_file)
            return True
        except OSError:
            QMessageBox.warning(None, "错误", "请使用管理员模式运行此工具")
            return False

    def get_launch_path(self):
        """Get the launch path from the configuration."""
        return self.config.get('PATH', 'launch_path', fallback=None)

    def set_launch_path(self, launch_path):
        """Set the launch path in the configuration."""
        if not self.config.has_section('PATH'):
            self.config.add_section('PATH')
        self.config.set('PATH', 'launch_path', launch_path)

    def get_accounts(self):
        """Get accounts from the configuration."""
        if self.config.has_section('ACCOUNTS'):
            return dict(self.config.items('ACCOUNTS'))
        return {}

    def set_accounts(self, accounts):
        """Set accounts in the configuration."""
        if self.config.has_section('ACCOUNTS'):
            self.config.remove_section('ACCOUNTS')
        self.config.add_section('ACCOUNTS')
        for account, password in accounts.items():
            self.config.set('ACCOUNTS', account, password)


class JsonLoader:
    def __init__(self, json_path):
        self.file_path = json_path
        self.data = self._load_data()
        self.indexed_data = {item["btn_name"]: item for item in self.data}

    def _load_data(self):
        with open(self.file_path, 'r', encoding="utf-8") as file:
            return json.load(file)

    def get_attribute(self, btn_name, attribute):
        item = self.indexed_data.get(btn_name)
        return item.get(attribute) if item else None
