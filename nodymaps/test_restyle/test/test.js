'use strict';
const chai = require('chai');
const assert = chai.assert;

function runRegex (fileContent) {
  const regexp = /\*\{background-repeat:no-repeat;padding:0;margin:0\}/g;
  const tagList = 'a|abbr|address|area|article|aside|audio|b|bdi|bdo|blockquote|br|button|canvas|caption|cite|code|col|colgroup|command|datalist|dd|del|details|dfn|div|dl|dt|em|embed|fieldset|figcaption|figure|footer|form|h1|h2|h3|h4|h5|h6|head|header|hgroup|hr|i|iframe|img|input|ins|kbd|keygen|label|legend|li|map|mark|menu|meter|nav|noscript|object|ol|optgroup|option|output|p|param|pre|progress|q|rp|rt|ruby|s|samp|section|select|small|source|span|strong|sub|summary|sup|table|tbody|td|textarea|tfoot|th|thead|time|tr|track|u|ul|var|video|wbr';
  const regexp2 = new RegExp(`(?<=^|\\}|,)(${tagList})(?=,|\\{)`, 'g');
  const regexp3 = /(?<=^|\}|,)(\[type=.+?\]|\[role=.+?\])(?=,|\{)/g;
  fileContent = fileContent.replace(regexp, '*{background-repeat:no-repeat;}');
  fileContent = fileContent.replace(regexp2, '.djeym $1');
  fileContent = fileContent.replace(regexp3, '.djeym $1');
  return fileContent;
}

const variations = [
  // *
  {
    text: '}*{background-repeat:no-repeat;padding:0;margin:0}',
    expected: '}*{background-repeat:no-repeat;}'
  },
  {
    text: '*{background-repeat:no-repeat;padding:0;margin:0}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '*{background-repeat:no-repeat;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  {
    text: '.v-tab{white-space:normal;}*{background-repeat:no-repeat;padding:0;margin:0}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '.v-tab{white-space:normal;}*{background-repeat:no-repeat;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  {
    text: '}*, :after, :before{background-repeat:no-repeat;padding:0;margin:0;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '}*, :after, :before{background-repeat:no-repeat;padding:0;margin:0;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  {
    text: '*, :after, :before{background-repeat:no-repeat;padding:0;margin:0;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '*, :after, :before{background-repeat:no-repeat;padding:0;margin:0;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  {
    text: '.v-tab{white-space:normal;}*, :after, :before{background-repeat:no-repeat;padding:0;margin:0;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '.v-tab{white-space:normal;}*, :after, :before{background-repeat:no-repeat;padding:0;margin:0;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  // div, a, button etc
  {
    text: 'button{background-color:transparent;border-style:none;color:inherit;}',
    expected: '.djeym button{background-color:transparent;border-style:none;color:inherit;}'
  },
  {
    text: 'button,input,select,textarea{background-color:transparent;border-style:none;color:inherit;}',
    expected: '.djeym button,.djeym input,.djeym select,.djeym textarea{background-color:transparent;border-style:none;color:inherit;}'
  },
  {
    text: '.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}button,input,select,textarea{background-color:transparent;border-style:none;color:inherit;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}.djeym button,.djeym input,.djeym select,.djeym textarea{background-color:transparent;border-style:none;color:inherit;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  {
    text: 'h2{display:block;font-size:1.5em;margin-block-start:0.83em;margin-block-end:0.83em;margin-inline-start:0px;margin-inline-end:0px;font-weight:bold;}',
    expected: '.djeym h2{display:block;font-size:1.5em;margin-block-start:0.83em;margin-block-end:0.83em;margin-inline-start:0px;margin-inline-end:0px;font-weight:bold;}'
  },
  // [type=] | [role=]
  {
    text: '[type=button],[type=reset],[type=submit][role=button],button{cursor:pointer;}',
    expected: '.djeym [type=button],.djeym [type=reset],.djeym [type=submit][role=button],.djeym button{cursor:pointer;}'
  },
  {
    text: '[type=button],[type=reset],[role=button][type=submit],button{cursor:pointer;}',
    expected: '.djeym [type=button],.djeym [type=reset],.djeym [role=button][type=submit],.djeym button{cursor:pointer;}'
  },
  {
    text: '.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}[type=button],[type=reset],[type=submit][role=button],button{cursor:pointer;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}',
    expected: '.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}.djeym [type=button],.djeym [type=reset],.djeym [type=submit][role=button],.djeym button{cursor:pointer;}.v-tabs:not(.v-tabs--vertical).v-tab{white-space:normal;}'
  },
  {
    text: '[type=button][type=submit][type=reset],[type=reset],[type=reset][role=button][type=submit],button{cursor:pointer;}',
    expected: '.djeym [type=button][type=submit][type=reset],.djeym [type=reset],.djeym [type=reset][role=button][type=submit],.djeym button{cursor:pointer;}'
  }
];

describe('runRegex', function () {
  function makeTest (text, expected) {
    it('restyle css', function () {
      assert.equal(runRegex(text), expected);
    });
  }

  variations.forEach(element => {
    makeTest(element.text, element.expected);
  });
});
