"use strict";

const fs = require("fs");
const pathFolder = "./dist/css/";
// *
const regexp = /\*\{background-repeat:no-repeat;padding:0;margin:0\}/g;
// div, a, button etc
const tagList =
  "a|abbr|address|area|article|aside|audio|b|bdi|bdo|blockquote|br|button|canvas|caption|cite|code|col|colgroup|command|datalist|dd|del|details|dfn|div|dl|dt|em|embed|fieldset|figcaption|figure|footer|form|h1|h2|h3|h4|h5|h6|head|header|hgroup|hr|i|iframe|img|input|ins|kbd|keygen|label|legend|li|map|mark|menu|meter|nav|noscript|object|ol|optgroup|option|output|p|param|pre|progress|q|rp|rt|ruby|s|samp|section|select|small|source|span|strong|sub|summary|sup|table|tbody|td|textarea|tfoot|th|thead|time|tr|track|u|ul|var|video|wbr";
const regexp2 = new RegExp(`(?<=^|\\}|,)(${tagList})(?=,|\\{)`, "g");
// [type=] | [role=]
const regexp3 = /(?<=^|\}|,)(\[type=.+?\]|\[role=.+?\])(?=,|\{)/g;

fs.readdirSync(pathFolder).forEach((file) => {
  let path = pathFolder + file;
  let fileContent = fs.readFileSync(path, "utf8");
  fileContent = fileContent.replace(regexp, "*{background-repeat:no-repeat;}"); // *
  fileContent = fileContent.replace(regexp2, ".djeym $1"); // div, a, button etc
  fileContent = fileContent.replace(regexp3, ".djeym $1"); // [type=] | [role=]
  fs.writeFileSync(path, fileContent);
});
