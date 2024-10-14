"""
Test main.py script
"""

from dotenv import load_dotenv
from databricks import sql
import os
import csv
from mylib.transform_load import (
    transform_voterreg,
    transform_votehistory,
    trim_dataset,
)
from mylib.extract import extract_zip


def test_extract_zip():
    """tests extract()"""
    try:
        # List all files in the specified directory
        directory = "data"
        files = os.listdir(directory)

        # Filter files that contain "nc" in their names
        nc_files = [file for file in files if "nc" in file]

        # Assert that there are exactly two files with "nc" in name
        assert (
            len(nc_files) == 2
        ), f"Expected 2 files with 'nc', found {len(nc_files)}: {nc_files}"

        print("Assertion passed: There are exactly two files with 'nc' in the name.")

    except AssertionError as e:
        print("Assertion failed:", e)
    except Exception as e:
        print("An error occurred:", e)


def test_load_voterreg():
    """tests transform and load functions"""
    directory = "data"
    dataset = f"{directory}/trimmed_voterreg.csv"
    payload = csv.reader(
        open(dataset, encoding="utf-16"),
        delimiter="\t",
    )
    # print(*payload)
    next(payload)
    load_dotenv()
    server_h = os.getenv("sql_server_host")
    access_token = os.getenv("databricks_api_key")
    http_path = os.getenv("sql_http")
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as conn:
        with conn.cursor() as c:
            # generate new table for the database
            c.execute("""SELECT * FROM ped19_voterreg """)
            result = c.fetchall()
            c.close()
            conn.close()
    assert result is not None


def test_load_votehistory():
    """tests transform and load functions"""
    directory = "data"
    dataset = f"{directory}/trimmed_voterhist.csv"
    payload = csv.reader(
        open(dataset, encoding="utf-16"),
        delimiter="\t",
    )
    # print(*payload)
    next(payload)
    load_dotenv()
    server_h = os.getenv("sql_server_host")
    access_token = os.getenv("databricks_api_key")
    http_path = os.getenv("sql_http")
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as conn:
        with conn.cursor() as c:
            # generate new table for the database
            c.execute("""SELECT * FROM ped19_voterhist """)
            result = c.fetchall()
            c.close()
            conn.close()
    assert result is not None


if __name__ == "__main__":
    extract_zip(
        url="https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter32.zip",
        directory="data",
    )
    extract_zip(
        url="https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvhis32.zip", directory="data"
    )
    main_directory = "/Users/pdeguz01/Documents/git/PeterdeGuzman_Mini6/"
    os.chdir(main_directory)
    transform_voterreg(
        txtfile=f"{main_directory}/data/ncvoter32.txt",
        county="Durham",
        date="241011",
        directory="data",
    )
    transform_votehistory(
        txtfile=f"{main_directory}/data/ncvhis32.txt",
        county="Durham",
        date="241011",
        directory="data",
    )
    trim_dataset(
        dataset=f"{main_directory}/data/voterreg_Durham241011.csv",
        dataset_type="voterreg",
        n=5000,
        directory="data",
    )
    trim_dataset(
        dataset=f"{main_directory}/data/votehist_Durham241011.csv",
        dataset_type="voterhist",
        n=5000,
        directory="data",
    )
    test_extract_zip()
    test_load_voterreg()
    test_load_votehistory()
