import re
import datetime
import pathlib
import configparser
import binascii
from typing import List
import logging

# setup logging
logger = logging.getLogger(__name__)


class Config():
    """
    Holds all confituration data readily available as attributes
    """
    def __init__(self, cfg_path: pathlib.Path) -> None:
        self.path_to_config_file = cfg_path
        self.read_config_file()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        # Deleting config during development. Comment after release.
        pass
    def read_config_file(self) -> None:
        """
        Reads current configuration file or creates a new one with a default configuration
        """
        self.config_parser = configparser.ConfigParser(allow_no_value=True)
        self.config_parser.optionxform = str
        try:
            self.config_parser.read_file(open(self.path_to_config_file))
            logger.debug(f"{self.path_to_config_file} read")
            self.parse()
        except FileNotFoundError:
            logger.info("config file missing")
            self.create_config_file()
    def create_config_file(self) -> None:
        """
        Creates the default config file
        """
        logger.debug(f"creating {self.path_to_config_file}")
        self.config_parser.add_section("Workflow")
        self.config_parser.set("Workflow", "# Define your workflow.")
        self.config_parser.set("Workflow", "# When you are done with your ticket analyses and ticket handling,")
        self.config_parser.set("Workflow", "# which of the ticket's attachments and extracted files do you want to keep on your harddrive?")
        self.config_parser.set("Workflow", "# \"\" = none, \"*\" = all, or enter a list of file masks, e.g. \"*.avi, *.zip, *.png, *.raw\"")
        self.config_parser.set("Workflow", "files_to_keep", "*")
        self.config_parser.add_section("Paths")
        self.config_parser.set("Paths", "# Set the absolute paths.")
        # self.config_parser.set("Paths", "path_to_tickets_folder", r"D:\trace")
        self.config_parser.set("Paths", "path_to_tickets_folder", r"G:\Sven\Python\mursili\traces")
        # self.config_parser.set("Paths", "path_to_tickets_folder", r"G:\trace")
        # self.config_parser.set("Paths", "path_to_hmi_monitor", r"D:\HMIMonitor-H42.237.4")
        self.config_parser.set("Paths", "path_to_hmi_monitor", r"G:\Sven\VW\HMIMonitor-H42.229.4")
        self.config_parser.set("Paths", "path_to_winrar_exe", r"C:\Program Files\WinRAR\WinRAR.exe")
        self.config_parser.add_section("Archives")
        self.config_parser.set("Archives", "# Archives will be extracted to a folder named after the archive")
        self.config_parser.set("Archives", "# To name the folder, we attach the 'extracted_dir_suffix' to the file name")
        self.config_parser.set("Archives", "extracted_dir_suffix", "_dir")
        self.config_parser.set("Archives", "# Archive suffixes")
        self.config_parser.set("Archives", "# Only write the suffix of the first archive part, i.e. no need for *.z01, *7z.002, etc.")
        self.config_parser.set("Archives", "zip_suffix", "*.zip")
        self.config_parser.set("Archives", "sevenzip_suffix", "*.7z, *.7z.001")
        self.config_parser.set("Archives", "rar_suffix", "*.rar")
        self.config_parser.set("Archives", "spilog_suffix", "*.spiLog")
        self.config_parser.add_section("Traces")
        self.config_parser.set("Traces", "# Trace-related settings")
        self.config_parser.set("Traces", "mlp_file_masks", "*MLP.raw, *_MLP_*.txt, *_MLP_*.raw, *Vlog*.txt, *54321.raw, *_Ethernet-2.raw")
        self.config_parser.set("Traces", "# Prefix to prepend to the concatenated trace file name")
        self.config_parser.set("Traces", "concatenated_trace_prefix", "Conc")
        self.config_parser.set("Traces", "# file name patterns to ignore for concatenation")
        self.config_parser.set("Traces", "avoid_concatenation", "*_OCU3_*")
        self.config_parser.set("Traces", "# Regular expression pattern of date and time in MLP file names")
        self.config_parser.set("Traces", "mlp_timestamp_pattern", r"(?P<from>\d{4}[0-2]\d[0-3]\d_[0-2]\d[0-5]\d[0-5]\d)_(?P<to>\d{4}[0-2]\d[0-3]\d_[0-2]\d[0-5]\d[0-5]\d)")
        self.config_parser.set("Traces", "# Timestamp format, see https://docs.python.org/3/library/time.html#time.strftime")
        self.config_parser.set("Traces", "# Escape % by %%, https://stackoverflow.com/a/31270121/9235421")
        self.config_parser.set("Traces", "mlp_timestamp_format", r"%%Y%%m%%d_%%H%%M%%S")
        self.config_parser.set("Traces", "# Maximal acceptable time gap between two consecutive MLP trace files (in s)")
        self.config_parser.set("Traces", "maximal_mlp_time_gap", "2")
        self.config_parser.set("Traces", "# Minimal acceptable time gap between two consecutive MLP trace files (in s)")
        self.config_parser.set("Traces", "minimal_mlp_time_gap", "0")
        self.config_parser.add_section("Telemotive_RAW")
        self.config_parser.set("Telemotive_RAW", "# Settings for Telemotive RAW format conversion")
        self.config_parser.set("Telemotive_RAW", "header", "| [VERSION] Telemotive-ASCII-Format Telemotive System Client v")
        self.config_parser.set("Telemotive_RAW", "line_start", "RX [RAW] -")
        self.config_parser.set("Telemotive_RAW", "marker", "MARKER")
        self.config_parser.set("Telemotive_RAW", "# Unescaped newline character(s), expecting either n or rn")
        self.config_parser.set("Telemotive_RAW", "tmraw_newline", "rn")
        self.config_parser.set("Telemotive_RAW", "unhexed_file_prefix", "Unhexed_")
        self.config_parser.add_section("KPM")
        self.config_parser.set("KPM", "# developer option to simulate download from KPM")
        # self.config_parser.set("KPM", "kpm_simul_path", r"G:\Sven\Python\mursili\KPMsimul")
        self.config_parser.set("KPM", "kpm_simul_path", r"D:\Python\mursili\KPMsimul")
        self.config_parser.add_section("Flask")
        self.config_parser.set("Flask", "# Webapp-related settings. Boolean values must be in lower case")
        self.config_parser.set("Flask", "flask_app_debug_mode", "false")
        self.config_parser.set("Flask", "flask_app_port", "7785")
        self.config_parser.add_section("Internal")
        self.config_parser.set("Internal", "# Internal program settings, change if you know what you are doing")
        self.config_parser.set("Internal", "# How often to ask external Winrar extractor if it is done extracting (in s)")
        self.config_parser.set("Internal", "process_polling_interval", "0.1")
        self.config_parser.set("Internal", "# How the MLP timstamp is written in the debug trace")
        self.config_parser.set("Internal", "trace_mlp_timestamp_format", r"%%H:%%M:%%S")
        self.config_parser.set("Internal", "# Report trace parsing progress each n lines")
        # self.config_parser.set("Internal", "trace_mlp_parsing_report_interval", "5")
        self.config_parser.set("Internal", "trace_mlp_parsing_report_interval", "157799")
        self.config_parser.set("Internal", "# Regular expression of the byte sequence delimiting two MLP records")
        with open(self.path_to_config_file, mode="w", encoding="utf-8") as configfh:
            self.config_parser.write(configfh)
        self.read_config_file()
    def delete_config_file(self) -> None:
        """
        Serves debugging purposes. Deletes the config file.
        """
        try:
            self.path_to_config_file.unlink()
            logger.debug(f"{self.path_to_config_file} deleted")
        except FileNotFoundError as exc:
            logger.exception(f"Could not delete {self.path_to_config_file}")
    def get_extensions(self, heading: str, key: str) -> List[str]:
        """
        Parses the extesions from config file, e.g.:
        "*.7z, *.7z.001" -> (".7z", ".001")
        """
        return tuple("." + extension.strip(" *").split(".")[-1] for extension in self.config_parser.get(heading, key).split(","))
    def get_bytes(self, heading: str, key: str) -> bytes:
        """
        Converts the string from the config file in to a bytes object.
        Uses utf-8 encoding
        """
        return bytes(self.config_parser.get(heading, key), encoding="utf-8")
        return binascii.unhexlify(self.config_parser.get(heading, key))
    def parse(self):
        """
        Parses the configuration files into usable attributes
        """
        self.files_to_keep = [item.strip() for item in self.config_parser.get("Workflow", "files_to_keep").split(",")]
        self.path_to_tickets_folder = pathlib.Path(self.config_parser.get("Paths", "path_to_tickets_folder"))
        self.path_to_hmi_monitor = pathlib.Path(self.config_parser.get("Paths", "path_to_hmi_monitor"))
        self.path_to_winrar_exe = pathlib.Path(self.config_parser.get("Paths", "path_to_winrar_exe"))
        self.extracted_dir_suffix = self.config_parser.get("Archives", "extracted_dir_suffix")
        self.zip_suffix = self.get_extensions("Archives", "zip_suffix")
        self.sevenzip_suffix = self.get_extensions("Archives", "sevenzip_suffix")
        self.rar_suffix = self.get_extensions("Archives", "rar_suffix")
        self.spilog_suffix = self.get_extensions("Archives", "spilog_suffix")
        self.archive_extensions = tuple(ext for ext in self.zip_suffix + self.sevenzip_suffix + self.rar_suffix + self.spilog_suffix)
        self.mlp_file_masks = [mask.strip() for mask in self.config_parser.get("Traces", "mlp_file_masks").split(",")]
        self.concatenated_trace_prefix = self.config_parser.get("Traces", "concatenated_trace_prefix")
        self.avoid_concatenation = [mask.strip() for mask in self.config_parser.get("Traces", "avoid_concatenation").split(",")]
        self.mlp_timestamp_pattern = re.compile(self.config_parser.get("Traces", "mlp_timestamp_pattern"))
        self.mlp_timestamp_format = self.config_parser.get("Traces", "mlp_timestamp_format")
        self.maximal_mlp_time_gap = datetime.timedelta(seconds=self.config_parser.getint("Traces", "maximal_mlp_time_gap"))
        self.minimal_mlp_time_gap = datetime.timedelta(seconds=self.config_parser.getint("Traces", "minimal_mlp_time_gap"))
        self.telemotive_raw_header = self.get_bytes("Telemotive_RAW", "header")
        self.telemotive_line_start = self.get_bytes("Telemotive_RAW", "line_start") + b" "
        self.telemotive_marker = self.get_bytes("Telemotive_RAW", "marker")
        self.telemotive_bytes_newline = self.get_bytes("Telemotive_RAW", "tmraw_newline").translate(bytes.maketrans(b"rn", b"\r\n"))
        self.telemotive_unhexed_file_prefix = self.config_parser.get("Telemotive_RAW", "unhexed_file_prefix")
        self.kpm_simul_path = pathlib.Path(self.config_parser.get("KPM", "kpm_simul_path"))
        self.process_polling_interval = self.config_parser.getfloat("Internal", "process_polling_interval")
        self.trace_mlp_timestamp_format = self.config_parser.get("Internal", "trace_mlp_timestamp_format")
        self.trace_mlp_parsing_report_interval = self.config_parser.getint("Internal", "trace_mlp_parsing_report_interval")
        self.flask_app_debug_mode = self.config_parser.getboolean("Flask", "flask_app_debug_mode")
        self.flask_app_port = self.config_parser.getint("Flask", "flask_app_port")


if __name__ == "__main__":
    pass
