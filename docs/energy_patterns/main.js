(function () {
"use strict";
    $(document).ready(function () {
        $.get('./patterns.yml')
        .done(function (data) {
          var patterns = jsyaml.load(data);

          Handlebars.registerHelper("total_occurrences", function(pattern) {
            var sum = 0;
            if(pattern.occurrences_android){
              if(pattern.occurrences_android.issues){
                sum += pattern.occurrences_android.issues.length
              }
              if(pattern.occurrences_android.commits){
                sum += pattern.occurrences_android.commits.length
              }
              if(pattern.occurrences_android.pull_requests){
                sum += pattern.occurrences_android.pull_requests.length
              }
            }
            if(pattern.occurrences_ios){
              if(pattern.occurrences_ios.issues){
                sum += pattern.occurrences_ios.issues.length
              }
              if(pattern.occurrences_ios.commits){
                sum += pattern.occurrences_ios.commits.length
              }
              if(pattern.occurrences_ios.pull_requests){
                sum += pattern.occurrences_ios.pull_requests.length
              }
            }
            return sum;
          });

          var source   = document.getElementById("pattern-template").innerHTML;
          var template = Handlebars.compile(source);
          var html = template(patterns);
          $("#patterns-list-placeholder").html(html);
      });
    });
}());
