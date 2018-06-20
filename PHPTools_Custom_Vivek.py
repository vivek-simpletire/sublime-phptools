import sublime, sublime_plugin
import os, os.path, time, subprocess
from os.path import dirname, realpath
# For taking backup of specific types of file saved in ST3
from shutil import copyfile
from datetime import datetime

MY_PLUGIN = dirname(realpath(__file__))
s = {}

class PHPTools(sublime_plugin.EventListener):
	def __init__(self):
		self.php_path = "php"
		self.formatter_path = MY_PLUGIN + "/php.tools/codeFormatter.php"
		self.debug = True
		self.psr = False

	def on_post_save_async(self, view):
		s = sublime.load_settings('PHPTools.sublime-settings')
		print("Settings: ", s)
		self.php_path = s.get("php_path", "php")
		self.formatter_path = s.get("formatter_path", MY_PLUGIN + "/php.tools/codeFormatter.php")
		self.debug = s.get("debug", False)
		self.psr = s.get("psr", False)

		full_file_name = view.file_name()
		folder_name, file_name = os.path.split(full_file_name)
		folder_name = folder_name.replace(" ", "\\ ")
		extension = os.path.splitext(full_file_name)[1][1:]

		if self.debug:
			print("ex ", extension, "folder: ", folder_name)

		psr_toggle = ""
		if self.psr:
			psr_toggle = "--psr"

		if "php" != extension:
			return False

		full_file_name_tmp = full_file_name + "-tmp"
		cmd = "\"{}\" \"{}\" {} \"{}\" > \"{}\"; \"{}\" -l \"{}\" && mv \"{}\" \"{}\";".format(
			self.php_path,
			self.formatter_path,
			psr_toggle,
			full_file_name,
			full_file_name_tmp,
			self.php_path,
			full_file_name_tmp,
			full_file_name_tmp,
			full_file_name
		)
		PHPTools().run(cmd, folder_name)

	def on_pre_save_async(self, view):
		full_file_name = view.file_name()
		folder_name, file_name = os.path.split(full_file_name)
		folder_name = folder_name.replace(" ", "\\ ")
		extension = os.path.splitext(full_file_name)[1][1:]
		# For taking backup of specific types of file saved in ST3
		allowedExtensions = ['php', 'js', 'ctp', 'phtml', 'xml', 'css', 'ini', 'py', 'sh', 'cmd', 'sql']

		if self.debug:
			print("ex ", extension, "folder: ", folder_name)

		# For taking backup of specific types of file saved in ST3 begin
		if extension in allowedExtensions:
			timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
			full_file_name_tmp = full_file_name + '-' + timestr + '-tmp'
			full_file_name_bak = full_file_name + '-' + timestr + '-bak'
			copyfile(full_file_name, full_file_name_tmp)
		# For taking backup of specific types of file saved in ST3 end

	def on_load_async(self, view):
		full_file_name = view.file_name()
		folder_name, file_name = os.path.split(full_file_name)
		folder_name = folder_name.replace(" ", "\\ ")
		extension = os.path.splitext(full_file_name)[1][1:]
		# For taking backup of specific types of file saved in ST3
		allowedExtensions = ['php', 'js', 'ctp', 'phtml', 'xml', 'css', 'ini', 'py', 'sh', 'cmd', 'sql']

		if self.debug:
			print("ex ", extension, "folder: ", folder_name)

		# For taking backup of specific types of file saved in ST3 begin
		if extension in allowedExtensions:
			timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
			full_file_name_tmp = full_file_name + '-' + timestr + '-tmp'
			full_file_name_bak = full_file_name + '-' + timestr + '-bak'
			copyfile(full_file_name, full_file_name_bak)
		# For taking backup of specific types of file saved in ST3 end

	def run(self, cmd, folder_name):
		if self.debug:
			print("Cmd ", cmd)

		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=folder_name, shell=True)
		result, err = p.communicate()
		if self.debug:
			if err:
				print("Error: ", err)
			else:
				print("Result: ", result)
