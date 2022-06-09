import fetch from "node-fetch";
import { createRequire } from "module";
const require = createRequire(import.meta.url);

const file = "mal_top3000.csv";
const fs = require("fs");
const baseURL = "https://api.jikan.moe/v4/top/anime";

fs.appendFileSync(file, "Mal_id,Score,Genres,Themes,Demographics\n");

async function recursiveWrite(iter) {
  if (iter > 120) {
    return;
  }

  await fetch(baseURL + "?page=" + iter)
    .then((response) => response.json())
    .then((data) => data.data)
    .then((data) => {
      data.forEach((animeData) => {
        const genres = [];
        const themes = [];
        const demographics = [];
        animeData.genres.forEach((obj) => genres.push(obj.name));
        animeData.themes.forEach((obj) => themes.push(obj.name));
        animeData.demographics.forEach((obj) => demographics.push(obj.name));

        fs.appendFileSync(file, "" + animeData.mal_id);
        fs.appendFileSync(file, "," + animeData.score);
        fs.appendFileSync(
          file,
          "," + '"' + JSON.stringify(genres).split('"').join("'") + '"'
        );
        fs.appendFileSync(
          file,
          "," + '"' + JSON.stringify(themes).split('"').join("'") + '"'
        );
        fs.appendFileSync(
          file,
          "," + '"' + JSON.stringify(demographics).split('"').join("'") + '"'
        );
        fs.appendFileSync(file, "\n");
      });
    });

  await setTimeout(() => recursiveWrite(iter + 1), 1000);
}

recursiveWrite(1);
