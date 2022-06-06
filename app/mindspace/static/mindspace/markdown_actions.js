var markdown_actions = {}

// var header1 = "# text-here"
var header1 = "# "
markdown_actions["Header 1"] = header1
// var header2 = "## text-here"
var header2 = "## "
markdown_actions["Header 2"] = header2
// var header3 = "### text-here"
var header3 = "### "
markdown_actions["Header 3"] = header3
// var bold = "**text-here**"
var bold = "****"
markdown_actions["Bold"] = bold
// var italic = "_text-here_"
var italic = "__"
markdown_actions["Italic"] = italic
// var quote = "> text-here"
var quote = "> "
markdown_actions["Quote"] = quote
var code = "`text-here`"
var code = "``"
markdown_actions["Code"] = code
var link = "[](url)"
markdown_actions["Link"] = link
// var bulleted = "- text-here"
var bulleted = "- "
markdown_actions["Bulleted List"] = bulleted
// var numbered = "1. text-here"
var numbered = "1. "
markdown_actions["Numbered List"] = numbered
// var check = "- [ ] text-here"
// var check = "- [ ] "
// markdown_actions["Checklist"] = check
var newline = "  \n"
markdown_actions["Line Break"] = newline

$.fn.selectRange = function(start, end) {
    if(end === undefined) {
        end = start;
    }
    return this.each(function() {
        if('selectionStart' in this) {
            this.selectionStart = start;
            this.selectionEnd = end;
        } else if(this.setSelectionRange) {
            this.setSelectionRange(start, end);
        } else if(this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd('character', end);
            range.moveStart('character', start);
            range.select();
        }
    });
};

$(document).ready(function() {
    $(".markdown-action").hover(function() {
        $(this).popover({
            content: $(this).data('value')
        }).popover('show');
    }, function() {
        $(this).popover('hide');
    });

    $(document).on("click", ".markdown-action", function(e) {
        e.stopImmediatePropagation();
        var act = $(this).data("value");
        var block = markdown_actions[act];
        var caretPos = $(".markdown-field:visible")[0].selectionStart;
        var textAreaTxt = $(".markdown-field:visible").val();

        if (caretPos !== 0) {
            $(".markdown-field:visible").val(textAreaTxt.substring(0, caretPos) + block + textAreaTxt.substring(caretPos));
        } else if (textAreaTxt.length > 0) {
            $(".markdown-field:visible").val(textAreaTxt + ' ' + block);
        } else {
            $(".markdown-field:visible").val(block);
        }

        $(".markdown-field:visible").focus();
        if (act === "Bold") {
            $(".markdown-field:visible").selectRange(caretPos + 2);
        } else if (act == "Italic" || act === "Code" || act === "Link") {
            $(".markdown-field:visible").selectRange(caretPos + 1);
        } else {
            $(".markdown-field:visible").selectRange(caretPos + block.length);
        }
    });
});