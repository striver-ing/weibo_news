from utils.export_data import ExportData
import time


def info_main():
    key_map = {
        'id': 'int__id',
        'site_id': 'int_site_id',
        'program_name': 'str_title',
        'content': 'clob_content',
        'program_url': 'str_url',
        'release_date': 'date_release_time',
        'image_url': 'str_image_url',
        'image_code': 'int_sexy_image_status',
        'video_download_url': 'str_video_download_url',
        'find_date': 'date_record_time',
        'OUT_CHAIN_STATUS': 'int_is_out_link'
    }

    export = ExportData('ZHEJIANG_CZVIDEO_info', 'TAB_VIDEO_PROGRAM_INFO', key_map, unique_key='PROGRAM_URL',
                        condition={'read_status': 0})#, 'site_id': 1023})#, "image_pron_status": 2})
    export.export_to_oracle()


if __name__ == '__main__':
    # db = OracleDB
    while True:
        info_main()
        time.sleep(300)

