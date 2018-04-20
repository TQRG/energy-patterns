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

          Handlebars.registerHelper("list_occurrences", function(occurrences_list) {
            console.log(occurrences_list)
            var html = $('<ul></ul>').addClass('list-group');
            occurrences_list.forEach(function(element){
              html.append($("<li><a href='"+element+"'>"+element+"</a></li>").addClass('list-group-item'));
            });
            return html.html();
          });

          var listPatterns = function () {
            var source   = document.getElementById("patterns-list-template").innerHTML;
            var template = Handlebars.compile(source);
            var html = template(patterns);
            $("#patterns-list-placeholder").html(html);
          }

          var viewPattern = function (name) {
            var patternData = patterns.find(x => x['name'] == unescape(name))
            var source   = document.getElementById("pattern-show-template").innerHTML;
            var template = Handlebars.compile(source);
            var html = template(patternData);
            $("#pattern-show-placeholder").html(html);
          };

          var routes = {
            '/patterns/': listPatterns,
            '/patterns/:name': viewPattern
          };

          var router = Router(routes).configure({'notfound':listPatterns});
          router.init();
        });
    });
}());
