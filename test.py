from SIA import (
    export_artikel5_name,
    export_artikel5_name_leagealSeatid,
    export_artikel5_uid,
)
from SIA_Nextcloud_Automation import creat_new_user, search_for_user


def test_compare_and_update():
    export_artikel5_name.compare_and_update(
        r"C:\coding\test_Data\artikel5_mail.csv",
        r"C:\coding\test_Data\results\artikel5_mail_results.csv",
    )


# test_compare_and_update()


def test_compare_and_update2():
    export_artikel5_name_leagealSeatid.compare_and_update(
        r"C:\coding\test_Data\artikel5_test_2.csv",
        r"C:\coding\test_Data\results\artikel5_test_results.csv",
    )


# test_compare_and_update2()


def test_compare_and_update_uid():
    export_artikel5_uid.compare_and_update(
        r"C:\coding\test_Data\artikel5_mail_uid.csv",
        r"C:\coding\test_Data\results\artikel5_mail_uid_results.csv",
    )


def test_export_shab():
    export_artikel5_uid.compare_and_update(
        r"C:\coding\test_Data\artikel5_mail_uid.csv",
        r"C:\coding\test_Data\results\artikel5_mail_uid_results.csv",
    )


# test_compare_and_update_uid()


def test_create_user_Cloud():

    creat_new_user.main(r"C:\coding\test_Data\nextcloud_test.CSV")


# test_create_user_Cloud()


def test_active_user_Cloud():

    search_for_user.main(r"C:\coding\test_Data\nextcloud_test.CSV")


# test_active_user_Cloud()
