/* ***** BEGIN LICENSE BLOCK *****
 * Distributed under the BSD license:
 *
 * Copyright (c) 2010, Ajax.org B.V.
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of Ajax.org B.V. nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL AJAX.ORG B.V. BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * ***** END LICENSE BLOCK ***** */

define(function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var JavaScriptHighlightRules = require("./javascript_highlight_rules").JavaScriptHighlightRules;
var HtmlHighlightRules = require("./html_highlight_rules").HtmlHighlightRules;

var ColdfusionHighlightRules = function() {
    HtmlHighlightRules.call(this);
    this.$rules.tag[2].token = function (start, tag) {
        var group = tag.slice(0,2) == "cf" ? "keyword" : "meta.tag";
        return ["meta.tag.punctuation." + (start == "<" ? "" : "end-") + "tag-open.xml",
            group + ".tag-name.xml"];
    }

    var jsAndCss = Object.keys(this.$rules).filter(function(x) {
        return /^(js|css)-/.test(x);
    });
    this.embedRules({
        cfmlComment: [
            { regex: "<!---", token: "comment.start", push: "cfmlComment"}, 
            { regex: "--->", token: "comment.end", next: "pop"},
            { defaultToken: "comment"}
        ]
    }, "", [
        { regex: "<!---", token: "comment.start", push: "cfmlComment"}
    ], [
        "comment", "start", "tag_whitespace", "cdata"
    ].concat(jsAndCss));
    
    
    this.$rules.cfTag = [
        {include : "attributes"},
        {token : "meta.tag.punctuation.tag-close.xml", regex : "/?>", next : "pop"}
    ];
    var cfTag = {
        token : function(start, tag) {
            return ["meta.tag.punctuation." + (start == "<" ? "" : "end-") + "tag-open.xml",
                "keyword.tag-name.xml"];
        },
        regex : "(</?)(cf[-_a-zA-Z0-9:.]+)",
        push: "cfTag"
    };
    jsAndCss.forEach(function(s) {
        this.$rules[s].unshift(cfTag);
    }, this);
    
    this.embedTagRules(new JavaScriptHighlightRules({jsx: false}).getRules(), "cfjs-", "cfscript");

    this.normalizeRules();
};

oop.inherits(ColdfusionHighlightRules, HtmlHighlightRules);

exports.ColdfusionHighlightRules = ColdfusionHighlightRules;
});
