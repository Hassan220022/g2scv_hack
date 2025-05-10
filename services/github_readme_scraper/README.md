# GitHub README Scraper

This service scrapes all README files from public repositories of a specified GitHub user and saves them as a JSON file in the bucket directory.

## Features

- Fetches all public repositories for a given GitHub username
- Extracts README content from each repository
- Stores comprehensive metadata including repository name, description, stars, and forks
- Saves all data as a well-structured JSON file in the bucket directory

## Requirements

- Python 3.6+
- GitHub Personal Access Token (set in `.env` file)

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with a GitHub username as an argument:

```bash
python main.py <github_username>
```

Example:

```bash
python main.py octocat
```

## Output

The script generates a JSON file in the bucket directory with the following format:
`<username>_github_readmes_<timestamp>.json`

Example output structure:

```json
 "Hassan220022/2-bit-alu": {
    "name": "2-bit-alu",
    "description": null,
    "stars": 0,
    "forks": 0,
    "last_updated": "2025-05-08T20:34:52",
    "languages": [
      "HTML",
      "Python",
      "TypeScript"
    ],
    "readme": "# 2-Bit ALU Design and Implementation\n\nThis project provides a comprehensive implementation of a 2-bit Arithmetic Logic Unit (ALU) using discrete 7400 series logic gates. It includes detailed hardware implementation guides, software simulation, and testing procedures.\n\n## Project Overview\n\nAn Arithmetic Logic Unit (ALU) is a fundamental component of any CPU, responsible for performing various arithmetic and logical operations. This project implements a simplified 2-bit ALU that can perform the following operations:\n\n- Bitwise AND\n- Bitwise OR\n- Bitwise XOR\n- Addition with carry\n- Subtraction using 2's complement\n- NOT (1's complement)\n\n```mermaid\ngraph TD\n    subgraph \"ALU Block Diagram\"\n        A[Input A] --> ALU\n        B[Input B] --> ALU\n        S[Operation Select] --> ALU\n        ALU --> R[Result]\n        ALU --> C[Carry/Borrow]\n    end\n```\n\n## Project Contents\n\n### Documentation\n- `docs/project_report.md`: Detailed project report with theoretical background and analysis\n- `hardware_design/circuit_implementation.md`: Step-by-step hardware implementation guide\n\n### Software Simulation\n- `src/alu_simulator.py`: Command-line simulation of the 2-bit ALU operations\n- `src/alu_visualizer.py`: GUI-based visualization showing ALU operations and circuit diagrams\n\n## Getting Started\n\n### Software Requirements\n- Python 3.6 or higher\n- Tkinter (for GUI visualization)\n- NumPy (for numerical operations)\n\n### Hardware Requirements\n- Breadboard\n- Logic Gate ICs:\n  - 1× 7408 ([Datasheet](https://www.ti.com/lit/ds/symlink/sn7408.pdf)): Quad 2-input AND gates\n  - 1× 7432 ([Datasheet](https://www.ti.com/lit/ds/symlink/sn7432.pdf)): Quad 2-input OR gates\n  - 1× 7486 ([Datasheet](https://www.ti.com/lit/ds/symlink/sn7486.pdf)): Quad 2-input XOR gates\n  - 1× 7404 ([Datasheet](https://www.ti.com/lit/ds/symlink/sn7404.pdf)): Hex inverter (NOT gates)\n- 6× SPDT switches for inputs\n- 3× LEDs with appropriate resistors (330Ohm)\n- 6× 10kOhm pull-up resistors\n- 4× 0.1uF decoupling capacitors\n- Jumper wires\n- 5V power supply\n\n### Installation\n\n1. Clone this repository:\n   ```\n   git clone https://github.com/yourusername/2-bit-alu.git\n   cd 2-bit-alu\n   ```\n\n2. Install required dependencies:\n   ```\n   pip install -r requirements.txt\n   ```\n\n### Running the Simulator\n\n1. Run the command-line simulator:\n   ```\n   python src/alu_simulator.py\n   ```\n\n2. Run the GUI visualizer:\n   ```\n   python src/alu_visualizer.py\n   ```\n\n### Building the Hardware\n\nSee the detailed instructions in `hardware_design/circuit_implementation.md`.\n\nThe basic steps are:\n1. Set up the power supply for all ICs\n2. Connect input switches with pull-up resistors\n3. Wire the logic gates according to the operation implementation diagrams\n4. Connect the output LEDs through current-limiting resistors\n\n```mermaid\ngraph TD\n    subgraph \"Basic Hardware Assembly Workflow\"\n        A[Set Up Power] --> B[Mount ICs on Breadboard]\n        B --> C[Wire Input Switches]\n        C --> D[Connect Logic Gates]\n        D --> E[Add Multiplexer Logic]\n        E --> F[Connect Output LEDs]\n        F --> G[Test Each Operation]\n    end\n```\n\n## Operation Codes\n\nThe ALU uses a 2-bit operation selector:\n\n| Operation | Op Code (S1:S0) | Description |\n|-----------|---------|-------------|\n| AND       | 00      | Bitwise AND |\n| OR        | 01      | Bitwise OR  |\n| XOR/ADD   | 10      | Addition with carry |\n| NOT/SUB   | 11      | Subtraction with borrow |\n\n## Example Operations\n\n### AND Operation Example\n```\nA = 10 (binary)\nB = 11 (binary)\nResult = 10 (binary)\n```\n\n### Addition Example\n```\nA = 10 (binary, decimal 2)\nB = 01 (binary, decimal 1)\nResult = 11 (binary, decimal 3)\n```\n\n### Subtraction Example\n```\nA = 11 (binary, decimal 3)\nB = 01 (binary, decimal 1)\nResult = 10 (binary, decimal 2)\n```\n\n## Circuit Diagram\n\n```mermaid\ngraph LR\n    subgraph \"Simplified Circuit\"\n        A[Inputs A/B] --> OPS[\"Operation Circuits<br/>(AND/OR/XOR/NOT)\"]\n        OPS --> MUX[Multiplexer]\n        S[Op Select] --> MUX\n        MUX --> R[Result]\n    end\n```\n\nFor detailed circuit diagrams, see `hardware_design/circuit_implementation.md`.\n\n## Troubleshooting\n\n### Common Issues and Solutions\n\n1. **No Power to ICs**\n   - Check +5V at pin 14 and GND at pin 7 of all ICs\n   - Verify power supply is providing 5V\n\n2. **Inconsistent Results**\n   - Add 0.1uF decoupling capacitors near each IC\n   - Check for floating inputs\n   - Verify pull-up resistors are properly connected\n\n3. **Switch Bounce Issues**\n   - Add debounce circuits (RC filters) to input switches\n\n## Video Demonstrations\n\n- [ALU Hardware Demo](https://youtube.com/example) (placeholder)\n- [Software Simulator Walkthrough](https://youtube.com/example) (placeholder)\n\n## Additional Resources\n\n- [Digital Logic Design Tutorial](https://www.tutorialspoint.com/digital_circuits/index.htm)\n- [Ben Eater's 8-bit Computer Series](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU)\n- [Online Logic Circuit Simulator](https://logic.ly/)\n- [TTL Logic Databook](https://www.ti.com/lit/sg/sdyu001ab/sdyu001ab.pdf)\n- [Interactive Simulator](https://claude.ai/public/artifacts/ea8579f5-8a7f-4332-8920-95c36823ea32)\n\n## Project Extensions\n\nWant to extend this project? Here are some ideas:\n\n1. Expand to 4-bit or 8-bit ALU\n2. Add multiplication and division operations\n3. Create a PCB design instead of breadboard\n4. Connect to a simple control unit to create a basic CPU\n5. Implement using a modern FPGA instead of discrete logic\n\n## License\n\nThis project is licensed under the MIT License - see the LICENSE file for details.\n\n## Acknowledgments\n\n- Course instructor and teaching assistants\n- Texas Instruments for 7400 series datasheets\n- Ben Eater's educational videos on digital logic"
  }
```

## Environment Variables

Create a `.env` file in the project root with your GitHub token:

```
GITHUB_TOKEN=your_github_personal_access_token
```

Note: The script will automatically use the token from the project's root `.env` file.
