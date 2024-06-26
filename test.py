from SIA import (
    export_artikel5_name,
    export_artikel5_name_leagealSeatid,
    export_artikel5_uid,
)


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


# test_compare_and_update_uid()
