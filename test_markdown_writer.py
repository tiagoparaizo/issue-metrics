"""A module containing unit tests for the write_to_markdown function in the markdown_writer module.

Classes:
    TestWriteToMarkdown: A class to test the write_to_markdown function with mock data.
    TestWriteToMarkdownWithEnv: A class to test the write_to_markdown function with
        environment variables set.

"""
import os
import unittest
from datetime import timedelta
from unittest.mock import mock_open, patch

from classes import IssueWithMetrics
from markdown_writer import write_to_markdown


class TestWriteToMarkdown(unittest.TestCase):
    """Test the write_to_markdown function."""

    def test_write_to_markdown(self):
        """Test that write_to_markdown writes the correct markdown file.

        This test creates a list of mock GitHub issues with time to first response
        attributes, calls write_to_markdown with the list and the average time to
        first response, time to close and checks that the function writes the correct
        markdown file.

        """
        # Create mock data
        issues_with_metrics = [
            IssueWithMetrics(
                "Issue 1",
                "https://github.com/user/repo/issues/1",
                timedelta(days=1),
                timedelta(days=2),
                timedelta(days=3),
                {"bug": timedelta(days=1)},
            ),
            IssueWithMetrics(
                "Issue 2\r",
                "https://github.com/user/repo/issues/2",
                timedelta(days=3),
                timedelta(days=4),
                timedelta(days=5),
                {"bug": timedelta(days=2)},
            ),
        ]
        average_time_to_first_response = timedelta(days=2)
        average_time_to_close = timedelta(days=3)
        average_time_to_answer = timedelta(days=4)
        average_time_in_labels = {"bug": "1 day, 12:00:00"}
        num_issues_opened = 2
        num_issues_closed = 1

        # Call the function
        write_to_markdown(
            issues_with_metrics=issues_with_metrics,
            average_time_to_first_response=average_time_to_first_response,
            average_time_to_close=average_time_to_close,
            average_time_to_answer=average_time_to_answer,
            average_time_in_labels=average_time_in_labels,
            num_issues_opened=num_issues_opened,
            num_issues_closed=num_issues_closed,
            labels=["bug"],
            search_query="is:issue is:open label:bug",
        )

        # Check that the function writes the correct markdown file
        with open("issue_metrics.md", "r", encoding="utf-8") as file:
            content = file.read()
        expected_content = (
            "# Issue Metrics"
            "| Metric | Value |"
            "| --- | ---: |"
            "| Average time to first response | 2 days, 0:00:00 |"
            "| Average time to close | 3 days, 0:00:00 |"
            "| Average time to answer | 4 days, 0:00:00 |"
            "| Average time spent in bug | 1 day, 12:00:00 |"
            "| Number of items that remain open | 2 |"
            "| Number of items closed | 1 |"
            "| Total number of items created | 2 |"
            "| Title | URL | Time to first response | Time to close |"
            " Time to answer | Time spent in bug |"
            "| --- | --- | --- | --- | --- | --- |"
            "| Issue 1 | https://github.com/user/repo/issues/1 | 1 day, 0:00:00 | "
            "2 days, 0:00:00 | 3 days, 0:00:00 | 1 day, 0:00:00 |"
            "| Issue 2 | https://github.com/user/repo/issues/2 | 3 days, 0:00:00 | "
            "4 days, 0:00:00 | 5 days, 0:00:00 | 2 days, 0:00:00 |"
            "_This report was generated with the [Issue Metrics Action](https://github.com/github/issue-metrics)_"
            "Search query used to find these items: `is:issue is:open label:bug`"
        )
        self.assertEqual(content, expected_content)
        os.remove("issue_metrics.md")

    def test_write_to_markdown_with_vertical_bar_in_title(self):
        """Test that write_to_markdown writes the correct markdown file when the title contains a vertical bar.

        This test creates a list of mock GitHub issues (one of which contains a vertical
        bar in the title) with time to first response attributes, calls write_to_markdown
        with the list and the average time to first response, time to close and checks
        that the function writes the correct markdown file.

        """
        # Create mock data
        issues_with_metrics = [
            IssueWithMetrics(
                "Issue 1",
                "https://github.com/user/repo/issues/1",
                timedelta(days=1),
                timedelta(days=2),
                timedelta(days=3),
                {"bug": timedelta(days=1)},
            ),
            IssueWithMetrics(
                "feat| Issue 2",  # title contains a vertical bar
                "https://github.com/user/repo/issues/2",
                timedelta(days=3),
                timedelta(days=4),
                timedelta(days=5),
                {"bug": timedelta(days=2)},
            ),
        ]
        average_time_to_first_response = timedelta(days=2)
        average_time_to_close = timedelta(days=3)
        average_time_to_answer = timedelta(days=4)
        average_time_in_labels = {"bug": "1 day, 12:00:00"}
        num_issues_opened = 2
        num_issues_closed = 1

        # Call the function
        write_to_markdown(
            issues_with_metrics=issues_with_metrics,
            average_time_to_first_response=average_time_to_first_response,
            average_time_to_close=average_time_to_close,
            average_time_to_answer=average_time_to_answer,
            average_time_in_labels=average_time_in_labels,
            num_issues_opened=num_issues_opened,
            num_issues_closed=num_issues_closed,
            labels=["bug"],
        )

        # Check that the function writes the correct markdown file
        with open("issue_metrics.md", "r", encoding="utf-8") as file:
            content = file.read()
        expected_content = (
            "# Issue Metrics"
            "| Metric | Value |"
            "| --- | ---: |"
            "| Average time to first response | 2 days, 0:00:00 |"
            "| Average time to close | 3 days, 0:00:00 |"
            "| Average time to answer | 4 days, 0:00:00 |"
            "| Average time spent in bug | 1 day, 12:00:00 |"
            "| Number of items that remain open | 2 |"
            "| Number of items closed | 1 |"
            "| Total number of items created | 2 |"
            "| Title | URL | Time to first response | Time to close |"
            " Time to answer | Time spent in bug |"
            "| --- | --- | --- | --- | --- | --- |"
            "| Issue 1 | https://github.com/user/repo/issues/1 | 1 day, 0:00:00 | "
            "2 days, 0:00:00 | 3 days, 0:00:00 | 1 day, 0:00:00 |"
            "| feat&#124; Issue 2 | https://github.com/user/repo/issues/2 | 3 days, 0:00:00 | "
            "4 days, 0:00:00 | 5 days, 0:00:00 | 2 days, 0:00:00 |"
            "_This report was generated with the [Issue Metrics Action](https://github.com/github/issue-metrics)_"
        )
        self.assertEqual(content, expected_content)
        os.remove("issue_metrics.md")

    def test_write_to_markdown_no_issues(self):
        """Test that write_to_markdown writes the correct markdown file when no issues are found."""
        # Call the function with no issues
        with patch("builtins.open", mock_open()) as mock_open_file:
            write_to_markdown(None, None, None, None, None, None, None)

        # Check that the file was written correctly
        expected_output = "no issues found for the given search criteria"
        mock_open_file.assert_called_once_with(
            "issue_metrics.md", "w", encoding="utf-8"
        )
        mock_open_file().write.assert_called_once_with(expected_output)


class TestWriteToMarkdownWithEnv(unittest.TestCase):
    """Test the write_to_markdown function with the HIDE* environment variables set."""

    def setUp(self):
        # Set the HIDE* environment variables to True
        os.environ["HIDE_TIME_TO_FIRST_RESPONSE"] = "True"
        os.environ["HIDE_TIME_TO_CLOSE"] = "True"
        os.environ["HIDE_TIME_TO_ANSWER"] = "True"
        os.environ["HIDE_LABEL_METRICS"] = "True"

    def tearDown(self):
        # Unset the HIDE* environment variables
        os.environ.pop("HIDE_TIME_TO_FIRST_RESPONSE")
        os.environ.pop("HIDE_TIME_TO_CLOSE")
        os.environ.pop("HIDE_TIME_TO_ANSWER")
        os.environ.pop("HIDE_LABEL_METRICS")

    def test_writes_markdown_file_with_non_hidden_columns_only(self):
        """
        Test that write_to_markdown writes the correct
        markdown file with non-hidden columns only.
        """

        # Create mock data
        issues_with_metrics = [
            IssueWithMetrics(
                title="Issue 1",
                html_url="https://github.com/user/repo/issues/1",
                time_to_first_response=timedelta(minutes=10),
                time_to_close=timedelta(days=1),
                time_to_answer=timedelta(hours=2),
                labels_metrics={
                    "label1": timedelta(days=1),
                },
            ),
            IssueWithMetrics(
                title="Issue 2",
                html_url="https://github.com/user/repo/issues/2",
                time_to_first_response=timedelta(minutes=20),
                time_to_close=timedelta(days=2),
                time_to_answer=timedelta(hours=4),
                labels_metrics={
                    "label1": timedelta(days=1),
                },
            ),
        ]
        average_time_to_first_response = timedelta(minutes=15)
        average_time_to_close = timedelta(days=1.5)
        average_time_to_answer = timedelta(hours=3)
        average_time_in_labels = {
            "label1": timedelta(days=1),
        }
        num_issues_opened = 2
        num_issues_closed = 1

        # Call the function
        write_to_markdown(
            issues_with_metrics=issues_with_metrics,
            average_time_to_first_response=average_time_to_first_response,
            average_time_to_close=average_time_to_close,
            average_time_to_answer=average_time_to_answer,
            average_time_in_labels=average_time_in_labels,
            num_issues_opened=num_issues_opened,
            num_issues_closed=num_issues_closed,
            labels=["label1"],
            search_query="repo:user/repo is:issue",
        )

        # Check that the function writes the correct markdown file
        with open("issue_metrics.md", "r", encoding="utf-8") as file:
            content = file.read()
        expected_content = (
            "# Issue Metrics"
            "| Metric | Value |"
            "| --- | ---: |"
            "| Number of items that remain open | 2 |"
            "| Number of items closed | 1 |"
            "| Total number of items created | 2 |"
            "| Title | URL |"
            "| --- | --- |"
            "| Issue 1 | https://github.com/user/repo/issues/1 |"
            "| Issue 2 | https://github.com/user/repo/issues/2 |"
            "_This report was generated with the [Issue Metrics Action](https://github.com/github/issue-metrics)_"
            "Search query used to find these items: `repo:user/repo is:issue`"
        )
        self.assertEqual(content, expected_content)
        os.remove("issue_metrics.md")
