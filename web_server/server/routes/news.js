var express = require("express");
var router = express.Router();
var request = require("request");

/* GET news listing. */
router.get("/userId/:userId/pageNum/:pageNum", function (req, res, next) {
  try {
    console.log("Fetching news...");
    user_id = req.params["userId"];
    page_num = req.params["pageNum"];

    var options = {
      method: "GET",
      url: `http://192.168.0.3:4040/getNewsSummariesForUser?user_id=${user_id}&page_num=${page_num}`,
      headers: {
        accept: "application/json",
      },
    };
    request(options, function (error, response) {
      if (error) return res.json(error.message);
      res.json(JSON.parse(response.body));
    });
  } catch (error) {
    res.json(error.message);
  }
});

/* Post news click event */
router.post("/userId/:userId/newsId/:newsId", (req, res, next) => {
  try {
    console.log("Logging news click...");
    user_id = req.params["userId"];
    news_id = req.params["newsId"];
    var options = {
      method: "GET",
      url: `http://172.16.238.10:4040/logNewsClickForUser?user_id=${user_id}&news_id=${news_id}`,
      headers: {
        accept: "application/json",
      },
    };
    request(options, function (error, response) {
      // res.json(JSON.parse(response.body));
    });
    res.json([]);
  } catch (error) {
    res.json(error.message);
  }
});

module.exports = router;
