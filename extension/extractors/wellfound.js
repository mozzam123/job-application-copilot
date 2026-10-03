class WellfoundExtractor {

  extract() {
    const jobDescription = this.extractJobDescription();

    return {
      company_name: this.extractCompanyName(),
      job_title: this.extractJobTitle(jobDescription),
      company_description: this.extractCompanyDescription(),
      job_description: jobDescription,
      requirements: this.extractRequirements(jobDescription),
      source_url: window.location.href
    };
  }

  extractJobTitle(jobDescription) {
    // Wellfound usually mentions the exact role near the beginning:
    // "As a Senior Software Engineer at Postscript..."
    if (jobDescription) {
      const match = jobDescription.match(
        /As an?\s+(.+?)\s+at\s+.+?,/i
      );

      if (match?.[1]) {
        return match[1].trim();
      }
    }

    // Fallback to browser title.
    const pageTitle = document.title;

    const patterns = [
      /^(.+?)\s+at\s+.+?\s*[|–-]/i,
      /^(.+?)\s+at\s+.+$/i
    ];

    for (const pattern of patterns) {
      const match = pageTitle.match(pattern);

      if (match?.[1]) {
        return match[1].trim();
      }
    }

    return null;
  }

  extractCompanyName() {
    const pageText = document.body.innerText;

    // Strong fallback:
    // "About the company\nPostscript"
    const aboutCompanyMatch = pageText.match(
      /About the company\s*\n+([^\n]+)/i
    );

    if (aboutCompanyMatch?.[1]) {
      return aboutCompanyMatch[1].trim();
    }

    // Another useful source:
    // "As a Senior Software Engineer at Postscript..."
    const aboutJob = this.extractJobDescription();

    if (aboutJob) {
      const jobMatch = aboutJob.match(
        /As an?\s+.+?\s+at\s+(.+?),/i
      );

      if (jobMatch?.[1]) {
        return jobMatch[1].trim();
      }
    }

    return null;
  }

  extractCompanyDescription() {
    const pageText = document.body.innerText;

    const match = pageText.match(
      /About the company\s*\n+([^\n]+)\s*\n+(?:Actively Hiring\s*\n+)?([^\n]+)/i
    );

    if (!match) {
      return null;
    }

    const companyName = match[1]?.trim();
    const description = match[2]?.trim();

    if (!description) {
      return companyName || null;
    }

    return description;
  }

  extractJobDescription() {
    return this.extractSection(
      ["About the job"],
      [
        "About the company",
        "Similar Jobs",
        "Other Jobs"
      ]
    );
  }

  extractRequirements(jobDescription) {
    if (!jobDescription) {
      return null;
    }

    const startHeadings = [
      "What We'll Love About You",
      "What We’ll Love About You",
      "Requirements",
      "Qualifications",
      "What We're Looking For",
      "What We’re Looking For"
    ];

    const endHeadings = [
      "What You'll Love About Us",
      "What You’ll Love About Us",
      "Benefits",
      "Perks"
    ];

    return this.extractTextBetweenHeadings(
      jobDescription,
      startHeadings,
      endHeadings
    );
  }

  extractSection(startHeadings, endHeadings) {
    const pageText = document.body.innerText;

    return this.extractTextBetweenHeadings(
      pageText,
      startHeadings,
      endHeadings
    );
  }

  extractTextBetweenHeadings(text, startHeadings, endHeadings) {
    const lowerText = text.toLowerCase();

    let startIndex = -1;
    let matchedStart = null;

    for (const heading of startHeadings) {
      const index = lowerText.indexOf(heading.toLowerCase());

      if (index !== -1) {
        startIndex = index;
        matchedStart = heading;
        break;
      }
    }

    if (startIndex === -1) {
      return null;
    }

    const contentStart = startIndex + matchedStart.length;

    let endIndex = text.length;

    for (const heading of endHeadings) {
      const index = lowerText.indexOf(
        heading.toLowerCase(),
        contentStart
      );

      if (index !== -1 && index < endIndex) {
        endIndex = index;
      }
    }

    const result = text
      .slice(contentStart, endIndex)
      .trim();

    return result || null;
  }
}