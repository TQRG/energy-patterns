(function () {
"use strict";
    $(document).ready(function () {
        $.get('./patterns.yml')
        .done(function (data) {
          console.log('File load complete');
          var patterns = jsyaml.load(data);
          console.log(patterns);
          var source   = document.getElementById("pattern-template").innerHTML;
          var template = Handlebars.compile(source);
          var html = template(patterns);
          $("#patterns-list-placeholder").html(html);
      });
    });
}());
