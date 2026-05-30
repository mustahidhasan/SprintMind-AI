from app.schemas.issue import GenerateIssueRequest


class LLMService:
    def generate_issue(self, payload: GenerateIssueRequest) -> dict:
        title = payload.rawTitle.strip()
        description = payload.rawDescription.strip()

        normalized_title = (
            f"Implement {title.lower()} flow" if 'implement' not in title.lower() else title
        )

        return {
            'title': normalized_title[:120],
            'description': f"Build a robust workflow for: {description}",
            'issueType': payload.preferredIssueType,
            'priority': payload.preferredPriority,
            'labels': ['ai-generated', 'productivity', 'sprintmind'],
            'acceptanceCriteria': [
                'Requirement is implemented as described',
                'Validation and error handling are included',
                'Behavior is testable with clear expected outcomes',
            ],
            'suggestedSubtasks': [
                'Design implementation approach',
                'Implement core functionality',
                'Add tests and validations',
            ],
            'confidence': 0.86,
        }
