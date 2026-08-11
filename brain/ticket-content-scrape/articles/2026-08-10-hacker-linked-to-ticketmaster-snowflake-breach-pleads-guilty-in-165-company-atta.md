---
title: "Hacker Linked to Ticketmaster Snowflake Breach Pleads Guilty in 165-Company Attack"
author: "Dave Clark"
source: "https://www.ticketnews.com/feed/"
url: "https://www.ticketnews.com/2026/08/hacker-linked-to-ticketmaster-snowflake-breach-pleads-guilty-in-165-company-attack/"
type: article
date: 2026-08-10
tags: [q2, q7, improve, build, ai-context, ticketmaster, snowflake, doj]
---

# Hacker Linked to Ticketmaster Snowflake Breach Pleads Guilty in 165-Company Attack

## Summary

Canadian hacker Connor Riley Moucka pleaded guilty Aug. 5 to federal charges tied to the 2024 Snowflake cloud-credential attack campaign that included the massive Ticketmaster data breach, admitting to computer fraud, wire fraud, aggravated identity theft and conspiracy; sentencing is set for Oct. 27.

### Key Points
- Attackers used stolen credentials (not a Snowflake platform vulnerability) to access at least 165 customer accounts lacking MFA between February and October 2024, stealing terabytes of data.
- The conspiracy generated more than $2.5 million in ransom payments (Moucka personally received about $495,000); DOJ puts victim-company direct losses above $9.5 million across at least 100 million affected customers.
- The 2024 Ticketmaster breach involved claims of up to 560 million customers' data and alleged ticket-barcode/inventory data, some of which Ticketmaster disputed, citing its rotating SafeTix barcodes.
- Co-defendant John Erin Binns remains outside U.S. custody; Moucka faces a two-year mandatory minimum on the identity-theft count and up to 30 years on the remaining counts.

### Highlights
- Guilty plea entered Aug. 5 to computer fraud, wire fraud, aggravated identity theft and conspiracy; sentencing Oct. 27.
- The campaign hit at least 165 companies via credential-stuffing against accounts lacking MFA -- not a Snowflake platform flaw -- underscoring that vendor/downstream account hygiene, not just platform security, drove the breach.
- DOJ: 100 million-plus customers' data implicated; $9.5 million-plus in direct victim-company losses; $2.5 million-plus extorted.

### Industry Problem
Third-party/cloud-vendor account compromise via stolen credentials (absent MFA) remains a live, material risk to ticketing platforms holding large PII/payment datasets -- a core patron-trust and fraud-defense pain point for any primary ticketing provider.

### Proposed Solution
The case underscores baseline defenses (mandatory MFA on all cloud-vendor accounts, credential rotation, anomaly detection on data-warehouse access) as non-negotiable; for Etix, this is a build/improve prompt to audit and harden third-party data-warehouse and analytics-vendor account security ahead of any breach, and to keep rotating/dynamic barcode tech (as Ticketmaster cites) as a mitigant against downstream ticket fraud even if account data leaks.

#q2 #q7 #improve #build #ai-context #ticketmaster #snowflake #doj

## Transcript

![Ticketmaster logo over a dark background with simulated computer code in green text.](https://www.ticketnews.com/wp-content/uploads/2024/05/Untitled-design-3.webp)

Ticketmaster logo over a dark background with simulated computer code in green text.

A Canadian hacker tied to the sprawling 2024 cyberattack campaign that included the massive Ticketmaster data breach has pleaded guilty to four federal charges, admitting his role in the theft of billions of sensitive records and an extortion scheme that collected millions of dollars from victim companies.

Connor Riley Moucka, 26, of Kitchener, Ontario, pleaded guilty Aug. 5 to computer fraud, wire fraud, aggravated identity theft and a related conspiracy, [according to the U.S. Department of Justice](https://www.justice.gov/usao-wdwa/united-states-vs-connor-riley-moucka-and-john-erin-binns). He is scheduled to be sentenced Oct. 27.

The plea marks a significant development in a hacking campaign that first drew widespread attention in the ticketing industry after data associated with hundreds of millions of Ticketmaster customers was offered for sale online in 2024.

According to prosecutors, Moucka and his co-conspirators used stolen login credentials between February and October 2024 to gain unauthorized access to cloud-hosted data belonging to at least 165 customers of a U.S.-based software-as-a-service company. The Justice Department does not name the cloud provider in its latest announcement, but the campaign has previously been identified as targeting customer accounts hosted by Snowflake.

Advertisement

  [<video width="728" height="90"><source src="https://www.ticketnews.com/wp-content/uploads/2026/05/processorqxislivebanner.webm" type="video/webm"> <source src="https://www.ticketnews.com/wp-content/uploads/2026/05/processorqxislivebanner.mp4" type="video/mp4"> Your browser does not support HTML5 video.</video>](https://processorqx.com?utm_source=TicketNews&utm_medium=banner&utm_campaign=processorqx "ProcessorQX is Live – A New Platform From Shows On Sale.")

That distinction has been a point of contention since the Ticketmaster breach first surfaced. Snowflake said in June 2024 that investigators had found no evidence that a vulnerability or security failure within its underlying platform caused the attacks. Instead, investigators said attackers appeared to be using credentials obtained elsewhere to target accounts that lacked multi-factor authentication.

Prosecutors now say the group used that access to steal terabytes of data containing billions of records, including financial information, payroll records, driver’s license and passport numbers, Social Security numbers, call and text-history records and other personally identifiable information.

The attackers then threatened to publish stolen information unless victims paid ransoms and separately advertised data for sale on cybercrime forums and Telegram, according to DOJ.

The conspiracy generated more than $2.5 million in ransom payments, with Moucka personally receiving at least $495,000, prosecutors said. DOJ puts the direct losses suffered by victim companies at more than $9.5 million, excluding losses suffered by their customers. Prosecutors said the affected companies collectively had at least 100 million individual customers whose information was implicated in the conduct admitted as part of the case.

Advertisement

  [<video width="728" height="90"><source src="https://www.ticketnews.com/wp-content/uploads/2026/04/InsomniacBanner_416.webm" type="video/webm"> <source src="https://www.ticketnews.com/wp-content/uploads/2026/04/insomniacbannermp4_416.mp4" type="video/mp4"> Your browser does not support HTML5 video.</video>](https://insomniacbrowser.com?utm_source=ticketnews&utm_medium=banner)

## Ticketmaster Breach Put Snowflake Campaign in Spotlight

TicketNews began covering the Snowflake attacks in May and June 2024 [after hackers advertised a massive cache of data purportedly taken from Ticketmaster](https://www.ticketnews.com/2024/07/hackers-leak-30k-ticketmaster-barcodes-share-tutorial-for-counterfeit-tickets/).

At the time, the group ShinyHunters claimed to possess approximately 1.3 terabytes of Ticketmaster data associated with as many as 560 million customers worldwide, including names, addresses, phone numbers, payment information and other account data. Live Nation Entertainment subsequently confirmed in an SEC filing that it had identified unauthorized activity in a third-party cloud database containing Ticketmaster data on May 20, although the company did not independently confirm all of the hackers’ claims about the scope of the stolen material.

Ticketmaster later notified affected customers that it had determined an unauthorized third party obtained information from a database hosted by a third-party data services provider. The company said its investigation placed the unauthorized activity between April 2 and May 18, 2024.

As the breach unfolded, hackers made additional claims involving Ticketmaster ticket inventory and barcodes, including assertions that they possessed hundreds of thousands of Taylor Swift tickets. Ticketmaster disputed some of those claims and said its rotating SafeTix barcodes could not simply be copied and reused.

The criminal investigation eventually put names to individuals prosecutors said were behind the broader Snowflake campaign.

Canadian authorities arrested Moucka in October 2024 at the request of the United States. He and alleged co-conspirator John Erin Binns were [subsequently indicted in the Western District of Washington](https://www.ticketnews.com/2024/11/two-indicted-for-snowflake-hack-that-led-to-ticketmaster-breach/) on charges involving computer fraud, wire fraud, aggravated identity theft and related conspiracies.

Moucka initially fought the U.S. case from Canada before consenting to surrender for extradition in March 2025. DOJ says he was extradited to the United States in July 2025, where he initially pleaded not guilty before changing his plea this month.

His guilty plea carries a mandatory minimum sentence of two years on the aggravated identity theft charge, while the remaining counts carry maximum penalties of up to 30 years in prison. The eventual sentence will be determined by a federal judge under federal sentencing guidelines.

The case is not entirely finished. Binns, Moucka’s co-defendant, is not currently in U.S. custody, according to the Justice Department’s case docket.
