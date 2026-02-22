module Jekyll
  class PatternPageGenerator < Generator
    safe true

    def generate(site)
      patterns = site.data["patterns"]
      return unless patterns

      patterns.each do |pattern|
        next unless pattern["name"]
        site.pages << PatternPage.new(site, site.source, pattern)
      end
    end
  end

  class PatternPage < Page
    def initialize(site, base, pattern)
      @site = site
      @base = base
      @dir  = "patterns"
      @name = Jekyll::Utils.slugify(pattern["name"]) + ".html"

      process(@name)
      read_yaml(File.join(base, "_layouts"), "pattern.html")

      data["pattern"]     = pattern
      data["title"]       = pattern["name"]
      data["description"] = pattern["description"]
      data["permalink"]   = "/patterns/#{Jekyll::Utils.slugify(pattern["name"])}/"
    end
  end
end
