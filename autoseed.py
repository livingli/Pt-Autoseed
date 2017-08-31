# ！/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Rhilip <rhilipruan@gmail.com>
# Licensed under the GNU General Public License v3.0


import logging
import sys
import time

from utils.connect import Connect
from utils.load.config import setting
from utils.load.handler import fileHandler, consoleHandler

# -*- Logging Model -*-
rootLogger = logging.getLogger('')  # Logging
rootLogger.setLevel(logging.NOTSET)
while rootLogger.handlers:  # Remove un-format logging in Stream, or all of messages are appearing more than once.
    rootLogger.handlers.pop()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(consoleHandler)

connect = Connect()  # Connect
if connect.reseed_tracker_list:  # TODO Check Please.
    logging.info("Initialization settings Success~")
else:
    sys.exit("None of autoseed is active,Exit.")
# -*- End of Loading Model -*-


def main():
    logging.info("Autoseed start~,will check database record at the First time.")
    last_id_check = connect.update_torrent_info_from_rpc_to_db(force_clean_check=True)
    i = 0
    while True:
        last_id_check = connect.update_torrent_info_from_rpc_to_db(last_id_check=last_id_check)  # 更新表
        connect.reseeders_update()  # reseed判断主函数
        if i % setting.delete_check_round == 0:
            connect.check_to_del_torrent_with_data_and_db()  # 清理种子

        sleep_time = setting.sleep_free_time
        if setting.busy_start_hour <= int(time.strftime("%H", time.localtime())) < setting.busy_end_hour:
            sleep_time = setting.sleep_busy_time

        logging.debug("Check time {ti} OK, Reach check id {cid},"
                      " Will Sleep for {slt} seconds.".format(ti=i, cid=last_id_check, slt=sleep_time))

        i += 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
