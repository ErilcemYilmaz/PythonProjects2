from SIA.artikel5 import (
    export_by_name,
    export_by_name_and_city,
    export_by_name_and_legal_seat_id,
    export_by_uid,
)
from SIA_Nextcloud_Automation import creat_new_user, search_for_user


def run_export_by_name():
    export_by_name.compare_and_update(
        r"C:\coding\test_Data\artikel5_mail.csv",
        r"C:\coding\test_Data\results\20241112_artikel5_mail_results.csv",
    )


def run_export_by_name_and_legal_seat_id():
    export_by_name_and_legal_seat_id.compare_and_update(
        r"C:\coding\test_Data\artikel5_test_2.csv",
        r"C:\coding\test_Data\results\20241112_artikel5_test_results.csv",
    )


def run_export_by_uid():
    export_by_uid.compare_and_update(
        r"C:\coding\test_Data\artikel5_mail_uid.csv",
        r"C:\coding\test_Data\results\20241112_artikel5_mail_uid_results.csv",
    )


def run_export_by_name_and_city():
    export_by_name_and_city.compare_and_update(
        r"C:\coding\test_Data\20240924_any_corporate_wo_UID.csv",
        r"C:\coding\test_Data\results\20240924_any_corporate_wo_UID_result_new.csv",
    )


def run_create_user_cloud():
    creat_new_user.main(r"C:\coding\test_Data\nextcloud_test.CSV")


def run_search_user_cloud():
    search_for_user.main(r"C:\coding\test_Data\nextcloud_test.CSV")


if __name__ == "__main__":
    # Uncomment the function you want to run
    run_export_by_name()
    # run_export_by_name_and_legal_seat_id()
    # run_export_by_uid()
    # run_export_by_name_and_city()
    # run_create_user_cloud()
    # run_search_user_cloud()
