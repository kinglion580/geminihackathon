#!/usr/bin/env python3
"""
EU AI Act Risk Classification Tool
===================================
Interactive tool to classify AI systems according to EU AI Act risk categories.

Usage:
    python ai_risk_classifier.py
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from datetime import datetime

console = Console()


class AIRiskClassifier:
    """Interactive classifier for EU AI Act risk assessment."""

    def __init__(self):
        self.system_info = {}
        self.classification_result = None

    def run(self):
        """Run the interactive classification process."""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]EU AI Act Risk Classification Tool[/bold cyan]\n"
            "Classify your AI system according to EU AI Act requirements\n"
            "[dim]Based on Regulation (EU) 2024/1689[/dim]",
            title="🇪🇺 AI Risk Classifier",
            border_style="cyan"
        ))

        # Gather system information
        self.gather_system_info()

        # Perform classification
        self.classify_system()

        # Display results
        self.display_results()

        # Offer to save report
        if Confirm.ask("\n💾 Would you like to save the assessment report?"):
            self.save_report()

    def gather_system_info(self):
        """Collect information about the AI system."""
        console.print("\n[bold yellow]Step 1: System Information[/bold yellow]")

        self.system_info['name'] = Prompt.ask("AI System Name")
        self.system_info['version'] = Prompt.ask("Version", default="1.0")
        self.system_info['description'] = Prompt.ask("Brief Description")

        console.print("\n[bold yellow]Step 2: Use Case Classification[/bold yellow]")

        # Check for prohibited practices
        console.print("\n[bold red]Prohibited Practices Check:[/bold red]")

        self.system_info['social_scoring'] = Confirm.ask(
            "Does the system perform general-purpose social scoring by public authorities?"
        )

        self.system_info['subliminal_manipulation'] = Confirm.ask(
            "Does the system use subliminal techniques to materially distort behavior?"
        )

        self.system_info['vulnerability_exploitation'] = Confirm.ask(
            "Does the system exploit vulnerabilities (age, disability, social situation)?"
        )

        self.system_info['facial_scraping'] = Confirm.ask(
            "Does the system scrape facial images from internet/CCTV for databases?"
        )

        self.system_info['emotion_workplace'] = Confirm.ask(
            "Does the system recognize emotions in workplace or education contexts?"
        )
        if self.system_info['emotion_workplace']:
            self.system_info['medical_safety_exception'] = Confirm.ask(
                "  Is it for medical or safety purposes?"
            )

        self.system_info['predictive_policing'] = Confirm.ask(
            "Does the system assess individual crime risk based solely on profiling?"
        )

        # Check for high-risk categories
        console.print("\n[bold orange1]High-Risk Categories Check:[/bold orange1]")

        categories = {
            'biometrics': "Remote biometric identification or emotion recognition",
            'critical_infrastructure': "Safety component for critical infrastructure (traffic, utilities)",
            'education': "Educational/vocational access, exam evaluation, or behavior assessment",
            'employment': "Recruitment, hiring, performance monitoring, or termination decisions",
            'essential_services': "Credit scoring, creditworthiness, or insurance risk assessment",
            'law_enforcement': "Individual risk assessment, evidence evaluation, or crime prediction",
            'migration': "Border control, asylum/visa processing, or risk assessment",
            'justice': "Judicial research, law application, or dispute resolution"
        }

        self.system_info['categories'] = []
        for cat_key, cat_desc in categories.items():
            if Confirm.ask(f"Does the system involve: {cat_desc}?"):
                self.system_info['categories'].append(cat_key)

        # Check for limited risk (transparency obligations)
        console.print("\n[bold yellow]Limited Risk Check:[/bold yellow]")

        limited_risk_types = {
            'chatbot': "Chatbot or conversational AI",
            'emotion_recognition': "Emotion recognition (outside prohibited contexts)",
            'deepfake': "Deepfake or synthetic content generation",
            'biometric_categorization': "Biometric categorization"
        }

        self.system_info['limited_risk_types'] = []
        for lr_key, lr_desc in limited_risk_types.items():
            if Confirm.ask(f"Is the system a: {lr_desc}?"):
                self.system_info['limited_risk_types'].append(lr_key)

        # Additional context
        console.print("\n[bold yellow]Additional Context:[/bold yellow]")

        self.system_info['deployment_context'] = Prompt.ask(
            "Deployment context",
            choices=["public-authority", "private-sector", "workplace", "education",
                    "healthcare", "law-enforcement", "general"],
            default="general"
        )

        self.system_info['affects_fundamental_rights'] = Confirm.ask(
            "Could the system affect fundamental rights (privacy, dignity, non-discrimination)?"
        )

    def classify_system(self):
        """Classify the system based on collected information."""

        # Check for prohibited practices
        if self._is_prohibited():
            self.classification_result = {
                'risk_level': 'UNACCEPTABLE',
                'color': 'bold red',
                'reasoning': self._get_prohibited_reasoning(),
                'requirements': ['System must NOT be deployed'],
                'compliance_actions': [
                    '❌ Discontinue development immediately',
                    '❌ Do not place system on the market',
                    '❌ Review for alternative approaches that comply with the regulation',
                    '⚖️ Consult legal counsel for compliance verification'
                ]
            }
            return

        # Check for high-risk
        if self.system_info['categories']:
            self.classification_result = {
                'risk_level': 'HIGH-RISK',
                'color': 'bold orange1',
                'reasoning': self._get_high_risk_reasoning(),
                'requirements': [
                    '✓ Implement risk management system (Article 9)',
                    '✓ Ensure data governance and quality (Article 10)',
                    '✓ Create technical documentation (Article 11, Annex IV)',
                    '✓ Implement automatic logging and record-keeping (Article 12)',
                    '✓ Ensure transparency and information to users (Article 13)',
                    '✓ Enable human oversight (Article 14)',
                    '✓ Ensure accuracy, robustness, and cybersecurity (Article 15)',
                    '✓ Conduct conformity assessment',
                    '✓ Register in EU database (if required)',
                    '✓ Maintain post-market monitoring system'
                ],
                'compliance_actions': self._get_high_risk_actions()
            }
            return

        # Check for limited risk
        if self.system_info['limited_risk_types']:
            self.classification_result = {
                'risk_level': 'LIMITED RISK',
                'color': 'bold yellow',
                'reasoning': 'System has transparency obligations under the EU AI Act',
                'requirements': [
                    '✓ Disclose AI interaction to users clearly',
                    '✓ Label AI-generated or manipulated content',
                    '✓ Inform users about emotion recognition or biometric categorization',
                    '✓ Ensure transparency about system capabilities and limitations'
                ],
                'compliance_actions': [
                    '📝 Implement clear disclosure mechanisms in UI/UX',
                    '📝 Add "AI-generated" or similar labels to outputs',
                    '📝 Update user documentation and terms of service',
                    '📝 Consider voluntary codes of conduct',
                    '📝 Monitor for regulatory updates'
                ]
            }
            return

        # Minimal risk
        self.classification_result = {
            'risk_level': 'MINIMAL RISK',
            'color': 'bold green',
            'reasoning': 'System does not fall under regulated high-risk or limited-risk categories',
            'requirements': [
                '✓ Consider voluntary codes of conduct',
                '✓ Apply responsible AI principles as best practice',
                '✓ Document risk assessment decision'
            ],
            'compliance_actions': [
                '📝 Document this classification decision',
                '📝 Consider implementing responsible AI principles voluntarily',
                '📝 Monitor for regulatory changes that might affect classification',
                '📝 Review classification if system functionality changes',
                '✅ No mandatory compliance requirements under EU AI Act'
            ]
        }

    def _is_prohibited(self):
        """Check if system falls under prohibited practices."""
        if self.system_info.get('social_scoring'):
            return True
        if self.system_info.get('subliminal_manipulation'):
            return True
        if self.system_info.get('vulnerability_exploitation'):
            return True
        if self.system_info.get('facial_scraping'):
            return True
        if self.system_info.get('predictive_policing'):
            return True
        if self.system_info.get('emotion_workplace') and not self.system_info.get('medical_safety_exception'):
            return True
        return False

    def _get_prohibited_reasoning(self):
        """Get reasoning for prohibited classification."""
        reasons = []
        if self.system_info.get('social_scoring'):
            reasons.append("General-purpose social scoring by public authorities (Article 5(1)(a))")
        if self.system_info.get('subliminal_manipulation'):
            reasons.append("Subliminal manipulation causing harm (Article 5(1)(a))")
        if self.system_info.get('vulnerability_exploitation'):
            reasons.append("Exploitation of vulnerabilities (Article 5(1)(b))")
        if self.system_info.get('facial_scraping'):
            reasons.append("Untargeted facial recognition scraping (Article 5(1)(h))")
        if self.system_info.get('predictive_policing'):
            reasons.append("Individual crime risk assessment based solely on profiling (Article 5(1)(d))")
        if self.system_info.get('emotion_workplace') and not self.system_info.get('medical_safety_exception'):
            reasons.append("Emotion recognition in workplace/education (Article 5(1)(f))")

        return "System falls under prohibited AI practices:\n  - " + "\n  - ".join(reasons)

    def _get_high_risk_reasoning(self):
        """Get reasoning for high-risk classification."""
        category_names = {
            'biometrics': 'Biometric identification and categorization',
            'critical_infrastructure': 'Critical infrastructure safety',
            'education': 'Education and vocational training',
            'employment': 'Employment and worker management',
            'essential_services': 'Essential private and public services',
            'law_enforcement': 'Law enforcement',
            'migration': 'Migration, asylum and border control',
            'justice': 'Administration of justice and democratic processes'
        }

        matched_categories = [category_names.get(cat, cat) for cat in self.system_info['categories']]

        return (
            "System falls under EU AI Act Annex III high-risk categories:\n  - " +
            "\n  - ".join(matched_categories)
        )

    def _get_high_risk_actions(self):
        """Get compliance actions for high-risk systems."""
        actions = [
            '📋 Establish comprehensive risk management system',
            '📋 Document all training data sources and governance procedures',
            '📋 Create Annex IV technical documentation',
            '📋 Implement automatic logging system',
            '📋 Create detailed instructions for users/deployers',
            '📋 Design and implement human oversight mechanisms',
            '📋 Conduct accuracy, robustness, and cybersecurity assessments',
            '📋 Perform conformity assessment (internal or third-party)',
            '📋 Prepare EU declaration of conformity',
            '📋 Affix CE marking'
        ]

        if 'biometrics' in self.system_info['categories']:
            actions.extend([
                '🔐 Conduct fundamental rights impact assessment',
                '🔐 Register system in EU database for high-risk AI'
            ])

        if self.system_info.get('affects_fundamental_rights'):
            actions.append('⚖️ Conduct additional fundamental rights assessment')

        return actions

    def display_results(self):
        """Display classification results."""
        result = self.classification_result

        console.print("\n\n")
        console.print("=" * 80)
        console.print(
            f"[{result['color']}]CLASSIFICATION RESULT: {result['risk_level']}[/{result['color']}]",
            justify="center"
        )
        console.print("=" * 80)

        # System info
        console.print(f"\n[bold]System:[/bold] {self.system_info['name']} v{self.system_info['version']}")
        console.print(f"[bold]Description:[/bold] {self.system_info['description']}")
        console.print(f"[bold]Assessment Date:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Reasoning
        console.print(f"\n[bold cyan]Reasoning:[/bold cyan]")
        console.print(result['reasoning'])

        # Requirements
        console.print(f"\n[bold cyan]Compliance Requirements:[/bold cyan]")
        for req in result['requirements']:
            console.print(f"  {req}")

        # Actions
        console.print(f"\n[bold cyan]Recommended Actions:[/bold cyan]")
        for action in result['compliance_actions']:
            console.print(f"  {action}")

        # Next steps
        if result['risk_level'] == 'HIGH-RISK':
            console.print("\n[bold yellow]⚠️  IMPORTANT - Next Steps:[/bold yellow]")
            console.print("  1. Review detailed requirements in EU AI Act Articles 8-15")
            console.print("  2. Use compliance checklist tool for systematic implementation")
            console.print("  3. Engage with legal counsel and conformity assessment bodies")
            console.print("  4. Plan for 6-36 month implementation timeline (depending on deadline)")
            console.print("  5. Budget for ongoing compliance and monitoring activities")

        console.print("\n" + "=" * 80 + "\n")

    def save_report(self):
        """Save assessment report to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ai_risk_assessment_{self.system_info['name'].replace(' ', '_')}_{timestamp}.md"
        filepath = Path(__file__).parent / filename

        report = self._generate_markdown_report()

        filepath.write_text(report, encoding='utf-8')
        console.print(f"\n[green]✓ Report saved to:[/green] {filepath}")

    def _generate_markdown_report(self):
        """Generate markdown report."""
        result = self.classification_result

        report = f"""# EU AI Act Risk Assessment Report

## System Information

- **System Name:** {self.system_info['name']}
- **Version:** {self.system_info['version']}
- **Description:** {self.system_info['description']}
- **Assessment Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Deployment Context:** {self.system_info['deployment_context']}

## Classification Result

### Risk Level: {result['risk_level']}

### Reasoning

{result['reasoning']}

## Compliance Requirements

"""
        for req in result['requirements']:
            report += f"- {req}\n"

        report += "\n## Recommended Actions\n\n"
        for action in result['compliance_actions']:
            report += f"- {action}\n"

        report += f"""

## Assessment Details

### Prohibited Practices Screening

- Social Scoring: {'Yes ❌' if self.system_info.get('social_scoring') else 'No ✓'}
- Subliminal Manipulation: {'Yes ❌' if self.system_info.get('subliminal_manipulation') else 'No ✓'}
- Vulnerability Exploitation: {'Yes ❌' if self.system_info.get('vulnerability_exploitation') else 'No ✓'}
- Facial Recognition Scraping: {'Yes ❌' if self.system_info.get('facial_scraping') else 'No ✓'}
- Emotion Recognition (Workplace/Education): {'Yes ❌' if self.system_info.get('emotion_workplace') and not self.system_info.get('medical_safety_exception') else 'No ✓'}
- Predictive Policing (Profiling-based): {'Yes ❌' if self.system_info.get('predictive_policing') else 'No ✓'}

### High-Risk Categories

"""
        if self.system_info['categories']:
            for cat in self.system_info['categories']:
                report += f"- {cat}\n"
        else:
            report += "- None identified\n"

        report += "\n### Limited Risk Types\n\n"
        if self.system_info['limited_risk_types']:
            for lr in self.system_info['limited_risk_types']:
                report += f"- {lr}\n"
        else:
            report += "- None identified\n"

        report += f"""

## Legal References

- **Regulation:** EU AI Act (Regulation (EU) 2024/1689)
- **Prohibited Practices:** Article 5
- **High-Risk AI Systems:** Articles 6-7, Annex III
- **Requirements for High-Risk Systems:** Articles 8-15
- **Transparency Obligations:** Article 50

## Next Steps

"""
        if result['risk_level'] == 'HIGH-RISK':
            report += """
1. **Immediate Actions** (0-3 months)
   - Engage legal counsel with EU AI Act expertise
   - Identify conformity assessment body if third-party assessment needed
   - Establish project governance structure
   - Begin gap analysis against Articles 8-15

2. **Short-term Actions** (3-12 months)
   - Implement risk management system
   - Establish data governance framework
   - Create technical documentation
   - Design human oversight mechanisms

3. **Medium-term Actions** (12-24 months)
   - Complete conformity assessment
   - Prepare EU declaration of conformity
   - Register in EU database (if applicable)
   - Establish post-market monitoring

4. **Ongoing**
   - Monitor regulatory updates and guidance
   - Maintain compliance documentation
   - Conduct periodic reviews and audits
"""
        elif result['risk_level'] == 'LIMITED RISK':
            report += """
1. Implement transparency disclosure mechanisms
2. Update user interfaces and documentation
3. Monitor for regulatory guidance on transparency requirements
4. Consider voluntary responsible AI practices
"""
        else:
            report += """
1. Document this risk classification decision
2. Monitor for regulatory changes
3. Review classification if system functionality changes
4. Consider voluntary responsible AI best practices
"""

        report += f"""

---

*This assessment is based on information provided and current understanding of EU AI Act requirements.
Consult with legal counsel for definitive compliance guidance.*

*Generated by EU AI Act Risk Classification Tool*
*Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        return report


def main():
    """Main entry point."""
    try:
        classifier = AIRiskClassifier()
        classifier.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Assessment cancelled.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
