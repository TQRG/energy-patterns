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
            if(occurrences_list != undefined){
              var html = $('<ul></ul>');//.addClass('list-group');
              occurrences_list.forEach(function(element){
                html.append($("<li>- <a href='"+element+"' target='_blank'>"+element+"</a></li>"));//.addClass('list-group-item'));
              });
              return '<ul class="list-unstyled">'+html.html()+'</ul>';
            }
          });
          
          Handlebars.registerHelper("list_references", function(references_list) {
            if(references_list != undefined){
              var html = $('<ul></ul>');
              references_list.forEach(function(element){
                html.append($("<li class='small'>- "+element.authors+" <a href='"+element.url+"' target='_blank'>"+element.title+"</a></li>"));//.addClass('list-group-item'));
              });
              return '<ul class="list-unstyled">'+html.html()+'</ul>';
            }
          });
          
          Handlebars.registerHelper("escape_pattern_name", function(name) {
              return name.replace(/ /g, '_');
          });

          var listPatterns = function () {
            if (window.patterns_list_template === undefined){
              var source = document.getElementById("patterns-list-template").innerHTML;
              window.patterns_list_template = Handlebars.compile(source);
            }
            var html = window.patterns_list_template(patterns);
            $("#main-content").html(html);
            $(".extra").show();
          }
          
          var notfound = function(){
            listPatterns()
          }
          
          var scroll_to_top = function(){
            // For Safari
            document.body.scrollTop = 0;
            // For Chrome, Firefox, IE and Opera
            document.documentElement.scrollTop = 0;
          }
          
          var unescape_pattern_name = function(name){
              return name.replace(/_/g, ' ');
          }

          var viewPattern = function (name) {
            var patternData = patterns.find(x => x['name'] == unescape_pattern_name(name));
            if (window.pattern_show_template === undefined){
              var source = document.getElementById("pattern-show-template").innerHTML;
              window.pattern_show_template = Handlebars.compile(source);
            }
            var html = window.pattern_show_template(patternData);
            $("#main-content").html(html);
            $('.extra').hide()
          };

          var routes = {
            '/patterns/': listPatterns,
            '/patterns/:name': viewPattern
          };

          var router = Router(routes).configure({'notfound':notfound, 'on': scroll_to_top});
          if(location.hash == ""){
            if(history.pushState) {
                history.pushState(null, null, '#/');
            }
            else {
                location.hash = '#/';
            }  
          }
          router.init()
        });
    });
}());
