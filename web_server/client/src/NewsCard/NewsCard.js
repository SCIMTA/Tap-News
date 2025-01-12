import "./NewsCard.css";

import React from "react";
import Auth from "../Auth/Auth";

class NewsCard extends React.Component {
  redirectToUrl(url) {
    this.sendClickLog();
    window.open(url, "_blank");
  }

  sendClickLog() {
    console.log(this.props.news.digest);
    let url = `http://localhost:3000/news/userId/${Auth.getEmail()}/newsId/${
      this.props.news.digest
    }`;

    let request = new Request(encodeURI(url), {
      method: "POST",
      headers: {
        Authorization: "bearer " + Auth.getToken(),
      },
      cache: "no-store",
    });

    fetch(request);
  }

  timeSTampToDate(timeStamp) {
    const date = new Date(timeStamp);
    return date.toLocaleDateString();
  }

  render() {
    const { description } = this.props.news;
    return (
      <div
        className="news-container"
        onClick={() => this.redirectToUrl(this.props.news.url)}
      >
        <div className="row">
          <div className="col s4 fill">
            <img src={this.props.news.urlToImage} alt="news" />
          </div>
          <div className="col s8">
            <div className="news-intro-col">
              <div className="new-intro-panel">
                <h4>{this.props.news.title.trim()}</h4>
                <div className="news-description">
                  <p>
                    {description.length > 250
                      ? description.substring(0, 250) + "..."
                      : description}
                  </p>
                  <div>
                    {this.props.news.source.id != null && (
                      <div className="chip light-blue news-chip">
                        {this.props.news.source.name}
                      </div>
                    )}
                    {this.props.news.reason != null && (
                      <div className="chip light-green news-chip">
                        {this.props.news.reason}
                      </div>
                    )}
                    {this.props.news.publishedAt != null && (
                      <div className="chip amber news-chip">
                        {this.timeSTampToDate(
                          this.props.news.publishedAt["$date"]
                        )}
                      </div>
                    )}
                    {this.props.news.score != null && (
                      <div className="chip light-red news-chip">
                        {this.props.news.score}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default NewsCard;
