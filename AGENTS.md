# Scheffer Sites - Psychology Landing Page Template

## Project purpose

This repository is a reusable landing page template for psychology professionals.

It is part of the Scheffer Sites production workflow and is intended to be reused as the starting point for client-specific websites.

The project should remain lightweight, responsive, accessible, SEO-friendly and easy to customize with verified client information.

## General working rules

- Preserve existing functionality unless the task explicitly requires changing it.
- Prefer targeted changes over unnecessary rewrites.
- Do not replace working architecture only to simplify implementation.
- Reuse existing components, tokens, patterns and project conventions whenever practical.
- Keep the implementation maintainable and understandable.
- Avoid adding dependencies, frameworks or libraries unless they provide a clear benefit and are explicitly justified.
- Do not introduce unrelated changes while completing a task.

## Scheffer Sites method skill

For tasks involving:

- project strategy;
- discovery and prioritization;
- information architecture;
- user journey;
- copy and conversion;
- CTA behavior;
- SEO;
- general accessibility;
- performance decisions;
- preview versus production;
- QA;
- publication and delivery;
- interpretation of reusable lessons from previous Scheffer Sites projects;

use the `scheffer-sites` skill located at:

`.agents/skills/scheffer-sites/`

This repository contains the operational copy of the Scheffer Sites Skill. The complete institutional Playbook and historical decision records are maintained centrally in the private repository `scheffergiro/scheffer-sites-playbook`.

Do not assume that the complete central Playbook is available inside a client repository. Use the bundled skill and its references for normal project work. Historical rationale should only be treated as available when the central Playbook is actually present in the Codex environment or its relevant material has been explicitly provided.

The skill must not turn a client-specific decision into a universal rule. Apply its principles to the actual client, niche, project constraints and verified information.

## Design skill

For tasks involving:

- visual design;
- art direction;
- layout;
- visual hierarchy;
- typography;
- colors;
- spacing;
- UI components;
- responsive adaptation;
- accessibility of visual interfaces;
- interaction design;
- visual QA;
- design-system decisions;

use the `codemakers-design` skill located at:

`.agents/skills/codemakers-design/`

Follow the project's requirements and client context before applying recommendations from the skill.

Do not blindly copy palettes, typography, layouts or reference studies from the skill. Use them as design guidance and adapt them to the actual client, content, audience and brand.

## How the skills work together

The `scheffer-sites` and `codemakers-design` skills are complementary.

Use `scheffer-sites` to coordinate the broader product and website method: strategy, journey, architecture, copy, conversion, SEO, accessibility, QA and publication.

Use `codemakers-design` as the specialist reference for visual direction, UI, layout, typography, spacing, responsive interface behavior, interaction details and visual QA.

For work that spans both areas, use both skills. Do not let either skill override explicit user requirements, verified client information, project-specific constraints or existing behavior that the task requires preserving.

When recommendations differ, identify the concrete project goal and choose the smallest justified solution rather than applying either skill mechanically.

## Template integrity

This repository may be used either as the reusable base template or as the starting point for a client-specific repository.

When working on the reusable template:

- keep structures reusable across different psychology professionals;
- avoid hardcoding information that belongs to one specific client;
- use clearly identifiable placeholders or configurable data where appropriate;
- avoid visual decisions that unnecessarily restrict future customization;
- do not convert the template into a website for a single professional unless explicitly requested.

When working on a client-specific repository:

- customization is allowed according to the client's confirmed identity, content and requirements;
- preserve reusable architecture where it does not conflict with the client's needs;
- do not assume that placeholder information from the template is factual client information.

## Client information

Never invent or infer professional information.

Only use client information that has been explicitly provided or verified.

This includes, but is not limited to:

- professional name;
- CRP;
- education;
- qualifications;
- therapeutic approach;
- specialties;
- target audience;
- professional experience;
- office address;
- service locations;
- online or in-person availability;
- phone number;
- WhatsApp;
- email;
- social media profiles;
- testimonials;
- ratings;
- certifications;
- associations;
- schedules;
- prices.

If required information is unavailable, preserve a placeholder or clearly mark the content as pending confirmation.

Never transform demonstration data into apparently verified factual information.

## Health-related content

This template is used for psychology professionals.

Content must not:

- promise therapeutic outcomes;
- guarantee improvement or treatment results;
- fabricate clinical claims;
- create invented testimonials;
- create invented credentials;
- make unsupported claims about mental health treatment.

Keep language professional, clear and appropriate for a healthcare-related service.

## Content

Preserve the client's intended meaning when editing copy.

Improve clarity, hierarchy and readability without introducing unsupported claims.

Avoid generic filler text when real content is available.

Do not rewrite substantial client content merely for stylistic variety unless requested.

For demonstration versions, make the demonstration status clear whenever a visitor could otherwise interpret an element as real client information.

## SEO

SEO is a core requirement of this template.

When modifying the page, preserve or improve:

- semantic HTML;
- heading hierarchy;
- page title;
- meta description;
- canonical information when configured;
- Open Graph metadata;
- structured data when applicable;
- meaningful link text;
- descriptive image alt text;
- crawlable textual content;
- performance;
- mobile usability.

Do not sacrifice semantic structure or useful content solely for visual presentation.

Avoid keyword stuffing.

Client-specific SEO information must be based on confirmed client data.

## Accessibility

Accessibility is a project requirement.

Preserve or improve:

- semantic HTML;
- keyboard navigation;
- visible focus states;
- appropriate ARIA attributes;
- sufficient color contrast;
- readable typography;
- accessible interactive controls;
- dialog behavior;
- menu behavior;
- reduced-motion support;
- appropriate alternative text.

Visual changes must not break existing accessible behavior.

Interactive elements must accurately represent what they do.

## Responsive behavior

Every relevant UI change must consider:

- mobile;
- tablet;
- desktop;
- narrow screens;
- long content;
- long professional names;
- long headings;
- zoom;
- keyboard navigation.

Do not treat responsiveness as simply shrinking the desktop layout.

Preserve content hierarchy and primary actions across viewport sizes.

## Images and assets

Do not invent or substitute photographs of the professional without explicit instruction.

Client photographs should only be used when provided or approved for the project.

Do not reuse a client's personal photograph in another client's project.

When an image is unavailable, use the project's intended placeholder behavior rather than fabricating a professional portrait.

Optimize images appropriately and preserve meaningful alternative text.

## WhatsApp and contact actions

Do not fabricate contact information.

If a valid WhatsApp number has not been provided, keep the existing demonstration or placeholder behavior.

Do not create a functional contact link using invented numbers or URLs.

When a real contact method is configured, ensure that the action clearly matches what the interface promises.

## Visual direction

Avoid making every psychology website visually identical.

The template provides structure, not a mandatory final identity.

When sufficient client information is available, visual decisions should reflect the individual professional's:

- positioning;
- audience;
- personality;
- therapeutic approach;
- communication style;
- existing visual identity.

Avoid automatically defaulting to generic wellness aesthetics.

## Implementation

Prefer the project's existing HTML, CSS, JavaScript and Python architecture.

Before introducing a new dependency, verify whether the requirement can reasonably be implemented with the existing stack.

Keep CSS organized and reuse existing variables or design tokens when possible.

Avoid unnecessary duplication.

Do not remove existing functionality merely because it is not involved in the current task.

## Validation

After substantial changes, verify the relevant parts of the project.

For visual or frontend changes, review at least:

- desktop layout;
- narrow/mobile layout;
- navigation;
- primary CTA;
- focus states;
- interactive components;
- content overflow;
- major responsive breakpoints.

For changes affecting design, use the `codemakers-design` review guidance when applicable.

For changes affecting SEO, verify that semantic structure and metadata remain valid.

For changes affecting Python generation or project utilities, run the relevant existing tests.

Do not claim that a test or visual validation was performed unless it was actually executed.

## Scope discipline

Only change files necessary to complete the requested task.

If a potential improvement is outside the requested scope, mention it separately instead of implementing it automatically.

Preserve unrelated existing work.

Before completing a substantial task, summarize:

1. what was changed;
2. which files were affected;
3. which validations were performed;
4. any relevant remaining limitation or pending client information.
