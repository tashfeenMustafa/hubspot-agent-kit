# HubSpot CRM Data Model Reference for AI Agents

This document provides a reference to key HubSpot CRM data models and properties relevant for AI agent interactions.

## 1. Contact Properties (Key Ones)

*   `email`: Primary email address.
*   `firstname`: Contact's first name.
*   `lastname`: Contact's last name.
*   `company`: Associated company name.
*   `phone`: Contact's phone number.
*   `lifecyclestage`: The contact's stage in the marketing and sales process (e.g., subscriber, lead, customer).
*   `hs_lead_status`: The contact's lead status (e.g., new, open, in_progress).
*   `utm_source`: UTM parameter: source of the traffic.
*   `utm_medium`: UTM parameter: medium of the traffic.
*   `utm_campaign`: UTM parameter: campaign name.
*   `utm_term`: UTM parameter: keyword used.
*   `utm_content`: UTM parameter: specific content that led to the click.
*   `hs_analytics_source`: HubSpot analytics property: original source of the contact.
*   `hs_analytics_source_data_1`: HubSpot analytics property: additional source data.
*   `hs_analytics_source_data_2`: HubSpot analytics property: additional source data.
*   `jobtitle`: Contact's job title.
*   `annualrevenue`: Company's annual revenue.
*   `numberofemployees`: Number of employees at the company.
*   `industry`: Industry of the company.
*   `hs_object_id`: Unique identifier for the contact.

## 2. Deal Properties

*   `dealname`: Name of the deal.
*   `dealstage`: Current stage of the deal in the sales pipeline.
*   `amount`: Monetary value of the deal.
*   `pipeline`: Sales pipeline the deal belongs to.
*   `closedate`: Date the deal is expected to close.
*   `hubspot_owner_id`: ID of the HubSpot owner assigned to the deal.
*   `hs_object_id`: Unique identifier for the deal.

## 3. Meeting Properties

*   `hs_meeting_title`: Title of the meeting.
*   `hs_meeting_body`: Description or notes of the meeting.
*   `hs_meeting_outcome`: Outcome of the meeting (e.g., booked, completed, no_show).
*   `hs_activity_type`: Type of activity (e.g., 'MEETING').
*   `hs_timestamp`: Timestamp of the meeting.
*   `hubspot_owner_id`: ID of the HubSpot owner of the meeting.

## 4. Call Properties

*   `hs_call_status`: Status of the call (e.g., completed, scheduled).
*   `hs_call_disposition`: Disposition of the call (e.g., connected, left_voicemail, no_answer).
*   `hs_call_duration`: Duration of the call in milliseconds.
*   `hs_call_body`: Notes or transcription of the call.
*   `hubspot_owner_id`: ID of the HubSpot owner of the call.

## 5. Lifecycle Stages (in order)

These represent the typical progression of a contact through the sales and marketing funnel:

1.  `subscriber`
2.  `lead`
3.  `marketingqualifiedlead` (MQL)
4.  `salesqualifiedlead` (SQL)
5.  `(Custom SAL - Sales Accepted Lead)`
6.  `opportunity`
7.  `customer`
8.  `evangelist`

## 6. Lead Status Values

These values further refine the stage of a lead within a given lifecycle stage, particularly for `lead` or `marketingqualifiedlead`:

*   `new`
*   `open`
*   `in_progress`
*   `open_deal`
*   `unqualified`
*   `attempted_to_contact`
*   `connected`
*   `bad_timing`

## 7. Object Type IDs

These numeric IDs are used in association APIs and some other contexts:

*   Contacts: `0-1`
*   Companies: `0-2`
*   Deals: `0-3`
*   Meetings: `0-47`
*   Calls: `0-48`

## 8. Association Type IDs

These IDs define the type of relationship between objects:

*   Contact to Deal: `4`
*   Deal to Contact: `3`
*   Contact to Company: `1`

## 9. Flow Types

Different types of HubSpot workflows are categorized by these flow types and their associated `objectTypeId`:

*   `CONTACT_FLOW`: Workflows based on contact properties and actions. (`objectTypeId: 0-1`)
*   `DEAL_FLOW`: Workflows based on deal properties and actions. (`objectTypeId: 0-3`)
*   `PLATFORM_FLOW`: Workflows based on other objects like Meetings or Calls. (`objectTypeId: 0-47` or `0-48` for meetings/calls respectively).