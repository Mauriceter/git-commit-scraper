# git-commit-scraper

A small tool to scrape email and potential sensitive info in commit from a github repo.

To use for external pentest on coporate repo.

```
python script.py <repository_url> [keywords]
```


### Example on NetExec repo:

![](screen/cmd-example.png)

Found commit with old password
![](screen/info-commit.png)

Got list of email from commit
![](screen/email.png)