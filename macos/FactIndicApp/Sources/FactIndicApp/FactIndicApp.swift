import AppKit
import Foundation
import SwiftUI
import UniformTypeIdentifiers

@main
struct FactIndicApp: App {
    var body: some Scene {
        WindowGroup {
            FactIndicWindow()
                .frame(minWidth: 1040, minHeight: 720)
                .preferredColorScheme(.dark)
        }
        .windowStyle(.titleBar)
        .defaultSize(width: 1240, height: 840)
    }
}

private enum Palette {
    static let background = Color(red: 0.043, green: 0.067, blue: 0.118)
    static let sidebar = Color(red: 0.059, green: 0.090, blue: 0.165)
    static let surface = Color(red: 0.075, green: 0.110, blue: 0.180)
    static let surfaceAlt = Color(red: 0.098, green: 0.141, blue: 0.220)
    static let hoverFill = Color(red: 0.118, green: 0.169, blue: 0.259)
    static let line = Color(red: 0.165, green: 0.224, blue: 0.325)

    static let ink = Color(red: 0.973, green: 0.980, blue: 0.988)
    static let secondaryInk = Color(red: 0.796, green: 0.835, blue: 0.882)
    static let muted = Color(red: 0.580, green: 0.639, blue: 0.722)

    static let green = Color(red: 0.176, green: 0.831, blue: 0.749)
    static let paleGreen = Color(red: 0.075, green: 0.275, blue: 0.265)
    static let amber = Color(red: 0.984, green: 0.749, blue: 0.141)
    static let paleAmber = Color(red: 0.250, green: 0.175, blue: 0.045)
    static let red = Color(red: 0.973, green: 0.443, blue: 0.443)
    static let paleRed = Color(red: 0.280, green: 0.095, blue: 0.115)
    static let blue = Color(red: 0.376, green: 0.647, blue: 0.980)
    static let paleBlue = Color(red: 0.090, green: 0.175, blue: 0.320)
}

private enum AppPage: String, CaseIterable, Identifiable {
    case overview = "Overview"
    case baselines = "Hindi baselines"
    case results = "Pilot results"
    case generation = "Generation metrics"
    case liveDemo = "Live demo & JSON"
    case tests = "Test suite"
    case method = "Method & limits"

    var id: String { rawValue }

    var symbol: String {
        switch self {
        case .overview: "house.fill"
        case .baselines: "chart.xyaxis.line"
        case .results: "chart.bar.xaxis"
        case .generation: "clock"
        case .liveDemo: "doc.text.magnifyingglass"
        case .tests: "checkmark.seal.fill"
        case .method: "text.book.closed"
        }
    }
}

private struct PilotResult: Identifiable {
    let model: String
    let prompt: String
    let supported: Int
    let minor: Int
    let major: Int
    let notes: String

    var id: String { "\(model)-\(prompt)" }
    var errors: Int { minor + major }
    var rate: Double { Double(errors) / 30.0 }

    static let all: [PilotResult] = [
        .init(model: "Qwen3 · 1.7B", prompt: "Standard", supported: 2, minor: 4, major: 24,
              notes: "Baseline standard prompt on 30 Roman-script Hinglish news articles. High rate of unsupported additions and entity/number drift."),
        .init(model: "Qwen3 · 1.7B", prompt: "Factuality-aware", supported: 4, minor: 8, major: 18,
              notes: "Paired difference vs. Standard: −6.7 pp (95% CI: −20.0 to +6.7 pp; includes zero). Shorter summaries (46.70 vs. 53.77 words)."),
        .init(model: "Qwen3 · 4B", prompt: "Standard", supported: 6, minor: 9, major: 15,
              notes: "Stronger baseline support than 1.7B, but 80.0% of outputs still received minor or major AI-screening error flags."),
        .init(model: "Qwen3 · 4B", prompt: "Factuality-aware", supported: 7, minor: 6, major: 17,
              notes: "Paired difference vs. Standard: −3.3 pp (95% CI: −13.3 to +6.7 pp; includes zero). Lowest overall error rate (76.7%) in the pilot.")
    ]
}

private struct GenerationCondition: Identifiable {
    let model: String
    let prompt: String
    let meanWords: String
    let meanCompression: String
    let corpusCompression: String
    let meanSeconds: String

    var id: String { "\(model)-\(prompt)" }

    static let all: [GenerationCondition] = [
        .init(model: "Qwen3 · 1.7B", prompt: "Standard", meanWords: "53.77", meanCompression: "0.7702", corpusCompression: "0.7696", meanSeconds: "4.540"),
        .init(model: "Qwen3 · 1.7B", prompt: "Factuality-aware", meanWords: "46.70", meanCompression: "0.6752", corpusCompression: "0.6684", meanSeconds: "3.032"),
        .init(model: "Qwen3 · 4B", prompt: "Standard", meanWords: "54.10", meanCompression: "0.7829", corpusCompression: "0.7743", meanSeconds: "4.750"),
        .init(model: "Qwen3 · 4B", prompt: "Factuality-aware", meanWords: "49.30", meanCompression: "0.7101", corpusCompression: "0.7056", meanSeconds: "4.126")
    ]
}

private struct InteractiveClaim: Codable, Identifiable {
    let claim: String
    let assessment: String
    let source_evidence: String?
    let quote_found_in_model_input: Bool?
    let independent_nli_label: String?
    let independent_nli_score: Double?

    var id: String { "\(claim)-\(assessment)" }
}

private struct InteractiveRunReport: Codable {
    let model: String?
    let prompt: String?
    let summary: String
    let summary_requires_manual_review: Bool?
    let summary_review_status: String?
    let factuality_status: String?
    let summary_generation_seconds: Double?
    let claim_check_seconds: Double?
    let claims: [InteractiveClaim]?

    static let sample = InteractiveRunReport(
        model: "Qwen/Qwen3-4B (Colab T4 · greedy)",
        prompt: "Factuality-aware Hinglish",
        summary: "Delhi Metro ne Tuesday ko 12 nayi electric buses shuru ki jo 3 routes par chalengi. Har bus me 42 seats hain, ek charge par 180 km chal sakti hai, aur minimum kiraya 15 rupees hai.",
        summary_requires_manual_review: false,
        summary_review_status: "passed_all_checks",
        factuality_status: "All 5 claims supported with verbatim source quotes",
        summary_generation_seconds: 3.42,
        claim_check_seconds: 1.85,
        claims: [
            InteractiveClaim(claim: "Delhi Metro launched 12 new electric buses on Tuesday.", assessment: "supported",
                             source_evidence: "Delhi Metro ne Tuesday ko 12 nayi electric buses shuru ki",
                             quote_found_in_model_input: true, independent_nli_label: "entailment", independent_nli_score: 0.994),
            InteractiveClaim(claim: "The buses will run on 3 routes and each has 42 seats.", assessment: "supported",
                             source_evidence: "jo 3 routes par chalengi. Har bus me 42 seats hain",
                             quote_found_in_model_input: true, independent_nli_label: "entailment", independent_nli_score: 0.989),
            InteractiveClaim(claim: "Each bus can run up to 180 km on one charge with a minimum fare of 15 rupees.", assessment: "supported",
                             source_evidence: "ek charge par 180 km tak chal sakti hai, jabki minimum kiraya 15 rupees rakha gaya hai.",
                             quote_found_in_model_input: true, independent_nli_label: "entailment", independent_nli_score: 0.992)
        ]
    )
}

private struct ChallengeSample: Identifiable {
    let id: String
    let title: String
    let source: String
    let qwen17: String
    let qwen4: String
    let nliNote: String

    static let all: [ChallengeSample] = [
        .init(id: "chandrayaan", title: "1. Single date + named entities",
              source: "Chandrayaan-3 ka Vikram lander 23 August 2023 ko Moon ke south pole par soft-land hua. Iske baad Pragyan rover lunar surface par utara aur scientific experiments shuru kiye.",
              qwen17: "Exact (2/2 supported, verbatim quotes)", qwen4: "Hit Colab GPU limit on final rerun", nliNote: "Entailment (0.997, 0.991)"),
        .init(id: "two-dates", title: "2. Two dates (guard stays off)",
              source: "ISRO ne 14 July 2023 ko Sriharikota se Chandrayaan-3 launch kiya tha. Karib 40 din baad, 23 August 2023 ko Vikram lander ne Moon par successful soft landing ki.",
              qwen17: "Exact (2/2 supported, verbatim quotes)", qwen4: "Exact (2/2 supported, verbatim quotes)", nliNote: "Entailment (0.997–0.998)"),
        .init(id: "numbers", title: "3. Number-heavy transit news",
              source: "Delhi Metro ne Tuesday ko 12 nayi electric buses shuru ki jo 3 routes par chalengi. Har bus me 42 seats hain aur ek charge par 180 km tak chal sakti hai, jabki minimum kiraya 15 rupees rakha gaya hai.",
              qwen17: "Kept digits, misread '12 nayi' as '12 November'", qwen4: "Exact (5/5 supported, all roles accurate)", nliNote: "Entailment / Neutral"),
        .init(id: "warning", title: "4. Explicit warning & negation",
              source: "Heavy rain ke baad administration ne alert jaari kiya hai ki log Yamuna nadi ke kinare bilkul na jaayein aur low-lying areas ko turant khali kar dein. Police ne bataya ki bridge par traffic band hai, isliye vehicles ko wahan se door rehne ko kaha gaya hai.",
              qwen17: "Preserved warning & direction (2/2)", qwen4: "Preserved warning & direction (4/4)", nliNote: "False-positive contradiction (0.682 / 0.902)"),
        .init(id: "weather", title: "5. Clean Hinglish (no numbers)",
              source: "Aaj subah Bengaluru me mausam kaafi suhana tha aur thandi hawa chal rahi thi. Office jaane wale logon ne bataya ki baarish ki wajah se kuch roads par traffic slow raha, lekin koi bada jam nahi laga.",
              qwen17: "Inverted 'kaafi suhana tha' to 'very hot and humid'", qwen4: "Exact (4/4 supported, 'quite pleasant')", nliNote: "Caught 1.7B error (contradiction, 0.784)")
    ]
}

private struct TestCaseResult: Identifiable {
    enum Status: String { case passed = "PASSED", failed = "FAILED", skipped = "SKIPPED", error = "ERROR" }
    let id = UUID()
    let file: String
    let name: String
    let status: Status
}

private final class TestRunner: ObservableObject {
    @Published var repoPath: String
    @Published var isRunning = false
    @Published var lastExitCode: Int32?
    @Published var rawOutput = ""
    @Published var summaryLine = "Not run yet · click Run All Tests"
    @Published var cases: [TestCaseResult] = []
    @Published var durationText: String?

    init() { self.repoPath = TestRunner.detectRepoPath() }

    static func detectRepoPath() -> String {
        let fm = FileManager.default
        let candidates = [
            URL(fileURLWithPath: Bundle.main.bundlePath).deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent().path,
            "/Users/sanchitsirohi/factindic",
            fm.currentDirectoryPath
        ]
        for path in candidates {
            let pyproject = (path as NSString).appendingPathComponent("pyproject.toml")
            let testsDir = (path as NSString).appendingPathComponent("tests")
            if fm.fileExists(atPath: pyproject) && fm.fileExists(atPath: testsDir) { return path }
        }
        return "/Users/sanchitsirohi/factindic"
    }

    var pythonPath: String {
        let venvPython = (repoPath as NSString).appendingPathComponent(".venv/bin/python")
        return FileManager.default.isExecutableFile(atPath: venvPython) ? venvPython : "/usr/bin/python3"
    }

    var passedCount: Int { cases.filter { $0.status == .passed }.count }
    var failedCount: Int { cases.filter { $0.status == .failed || $0.status == .error }.count }

    func chooseRepoFolder() {
        let panel = NSOpenPanel()
        panel.canChooseDirectories = true
        panel.canChooseFiles = false
        panel.allowsMultipleSelection = false
        panel.message = "Select the FactIndic repository root (containing pyproject.toml and tests/)"
        if panel.runModal() == .OK, let url = panel.url { repoPath = url.path }
    }

    func runTests(target: String = "tests") {
        guard !isRunning else { return }
        let testsPath = (repoPath as NSString).appendingPathComponent(target)
        guard FileManager.default.fileExists(atPath: testsPath) else {
            rawOutput = "Tests path not found: \(testsPath)"
            summaryLine = "Repository path not found"
            lastExitCode = 1
            return
        }
        isRunning = true
        summaryLine = "Running pytest…"
        rawOutput = ""
        cases = []
        durationText = nil
        lastExitCode = nil
        let python = pythonPath
        let cwd = repoPath
        let start = Date()

        DispatchQueue.global(qos: .userInitiated).async {
            let process = Process()
            process.executableURL = URL(fileURLWithPath: python)
            process.arguments = ["-m", "pytest", "-v", "-p", "no:cacheprovider", target]
            process.currentDirectoryURL = URL(fileURLWithPath: cwd)
            var env = ProcessInfo.processInfo.environment
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            process.environment = env
            let pipe = Pipe()
            process.standardOutput = pipe
            process.standardError = pipe
            do {
                try process.run()
                let data = pipe.fileHandleForReading.readDataToEndOfFile()
                process.waitUntilExit()
                let elapsed = Date().timeIntervalSince(start)
                let output = String(data: data, encoding: .utf8) ?? ""
                let parsed = Self.parsePytestOutput(output)
                let exit = process.terminationStatus
                DispatchQueue.main.async {
                    self.rawOutput = output
                    self.cases = parsed
                    self.lastExitCode = exit
                    self.durationText = String(format: "%.2f s", elapsed)
                    let passed = parsed.filter { $0.status == .passed }.count
                    let failed = parsed.filter { $0.status == .failed || $0.status == .error }.count
                    self.summaryLine = exit == 0 ? "\(passed) passed in \(String(format: "%.2f s", elapsed))"
                        : (failed > 0 ? "\(failed) failed, \(passed) passed" : "Exited with code \(exit)")
                    self.isRunning = false
                }
            } catch {
                DispatchQueue.main.async {
                    self.rawOutput = "Failed to launch \(python): \(error.localizedDescription)"
                    self.summaryLine = "Launch failed"
                    self.lastExitCode = 1
                    self.isRunning = false
                }
            }
        }
    }

    func runVerifySetup() {
        guard !isRunning else { return }
        let scriptPath = (repoPath as NSString).appendingPathComponent("verify_setup.py")
        guard FileManager.default.fileExists(atPath: scriptPath) else {
            rawOutput = "verify_setup.py not found in \(repoPath)"
            summaryLine = "verify_setup.py missing"
            lastExitCode = 1
            return
        }
        isRunning = true
        summaryLine = "Running verify_setup.py…"
        rawOutput = ""
        cases = []
        durationText = nil
        lastExitCode = nil
        let python = pythonPath
        let cwd = repoPath
        let start = Date()

        DispatchQueue.global(qos: .userInitiated).async {
            let process = Process()
            process.executableURL = URL(fileURLWithPath: python)
            process.arguments = ["verify_setup.py"]
            process.currentDirectoryURL = URL(fileURLWithPath: cwd)
            let pipe = Pipe()
            process.standardOutput = pipe
            process.standardError = pipe
            do {
                try process.run()
                let data = pipe.fileHandleForReading.readDataToEndOfFile()
                process.waitUntilExit()
                let elapsed = Date().timeIntervalSince(start)
                let output = String(data: data, encoding: .utf8) ?? ""
                let exit = process.terminationStatus
                DispatchQueue.main.async {
                    self.rawOutput = output
                    self.lastExitCode = exit
                    self.durationText = String(format: "%.2f s", elapsed)
                    self.summaryLine = exit == 0 ? "Environment verified in \(String(format: "%.2f s", elapsed))" : "Exited with code \(exit)"
                    self.isRunning = false
                }
            } catch {
                DispatchQueue.main.async {
                    self.rawOutput = "Failed to launch \(python): \(error.localizedDescription)"
                    self.summaryLine = "Launch failed"
                    self.lastExitCode = 1
                    self.isRunning = false
                }
            }
        }
    }

    private static func parsePytestOutput(_ output: String) -> [TestCaseResult] {
        var results: [TestCaseResult] = []
        for line in output.split(separator: "\n", omittingEmptySubsequences: true) {
            let text = String(line)
            guard text.contains("::") else { continue }
            let status: TestCaseResult.Status? = text.contains(" PASSED") ? .passed
                : (text.contains(" FAILED") ? .failed
                : (text.contains(" SKIPPED") ? .skipped
                : (text.contains(" ERROR") ? .error : nil)))
            guard let resolvedStatus = status else { continue }
            let leftPart = text.components(separatedBy: " \(resolvedStatus.rawValue)").first ?? text
            let parts = leftPart.components(separatedBy: "::")
            let file = parts.first?.replacingOccurrences(of: "tests/", with: "") ?? "tests"
            let name = parts.dropFirst().joined(separator: "::")
            results.append(TestCaseResult(file: file, name: name, status: resolvedStatus))
        }
        return results
    }
}

private struct HandCursorOnHover: ViewModifier {
    let enabled: Bool
    func body(content: Content) -> some View {
        content.onHover { isHovering in
            guard enabled else { return }
            if isHovering { NSCursor.pointingHand.push() } else { NSCursor.pop() }
        }
    }
}

private extension View {
    func pointingHand(_ enabled: Bool = true) -> some View { modifier(HandCursorOnHover(enabled: enabled)) }
}

private struct MetricCard: View {
    let value: String
    let title: String
    let detail: String
    var accent: Color = Palette.green
    var actionHint: String? = nil
    var action: (() -> Void)? = nil
    @State private var isHovering = false

    var body: some View {
        Group {
            if let action {
                Button(action: action) { cardContent }
                    .buttonStyle(.plain)
                    .pointingHand()
                    .onHover { isHovering = $0 }
            } else {
                cardContent
            }
        }
    }

    private var cardContent: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .firstTextBaseline) {
                Text(value).font(.system(size: 30, weight: .bold, design: .rounded)).foregroundStyle(accent)
                Spacer()
                if let actionHint {
                    HStack(spacing: 3) { Text(actionHint); Image(systemName: "arrow.up.right") }
                        .font(.system(size: 10, weight: .semibold))
                        .foregroundStyle(isHovering ? accent : Palette.muted)
                }
            }
            Text(title).font(.system(size: 13.5, weight: .semibold)).foregroundStyle(Palette.ink)
            Text(detail).font(.system(size: 12)).foregroundStyle(Palette.muted).fixedSize(horizontal: false, vertical: true)
        }
        .frame(maxWidth: .infinity, minHeight: 118, alignment: .leading)
        .padding(18)
        .background(isHovering && action != nil ? Palette.hoverFill : Palette.surface, in: RoundedRectangle(cornerRadius: 14))
        .overlay(RoundedRectangle(cornerRadius: 14).stroke(isHovering && action != nil ? accent.opacity(0.75) : Palette.line, lineWidth: isHovering && action != nil ? 1.5 : 1))
    }
}

private struct HeaderTag: View {
    let text: String
    var tone: Color = Palette.green
    var background: Color = Palette.paleGreen

    var body: some View {
        Text(text)
            .font(.system(size: 10, weight: .bold, design: .monospaced))
            .tracking(0.9)
            .foregroundStyle(tone)
            .padding(.horizontal, 11)
            .padding(.vertical, 6)
            .background(background, in: Capsule())
            .overlay(Capsule().stroke(tone.opacity(0.35), lineWidth: 1))
    }
}

private struct NoticeCard: View {
    enum Tone { case amber, green, red, blue }
    let title: String
    let message: String
    let tone: Tone

    private var iconName: String {
        switch tone {
        case .amber: "exclamationmark.triangle.fill"
        case .green: "checkmark.circle.fill"
        case .red: "xmark.octagon.fill"
        case .blue: "info.circle.fill"
        }
    }
    private var accentColor: Color {
        switch tone { case .amber: Palette.amber; case .green: Palette.green; case .red: Palette.red; case .blue: Palette.blue }
    }
    private var bgColor: Color {
        switch tone { case .amber: Palette.paleAmber; case .green: Palette.paleGreen; case .red: Palette.paleRed; case .blue: Palette.paleBlue }
    }

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: iconName).font(.system(size: 16)).foregroundStyle(accentColor).padding(.top, 2)
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.system(size: 13.5, weight: .semibold)).foregroundStyle(accentColor)
                Text(message).font(.system(size: 12.5)).lineSpacing(3).foregroundStyle(Palette.secondaryInk).fixedSize(horizontal: false, vertical: true)
            }
            Spacer(minLength: 0)
        }
        .padding(15)
        .background(bgColor, in: RoundedRectangle(cornerRadius: 13))
        .overlay(RoundedRectangle(cornerRadius: 13).stroke(accentColor.opacity(0.4), lineWidth: 1))
    }
}

private struct FactIndicWindow: View {
    @State private var page: AppPage = .overview
    @StateObject private var testRunner = TestRunner()

    var body: some View {
        HStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 0) {
                VStack(alignment: .leading, spacing: 4) {
                    Text("FactIndic").font(.system(size: 20, weight: .bold, design: .rounded)).foregroundStyle(Palette.ink)
                    Text("CSET 346 · NLP PROJECT").font(.system(size: 9.5, weight: .bold, design: .monospaced)).tracking(1.0).foregroundStyle(Palette.green)
                }
                .padding(.horizontal, 18).padding(.top, 20).padding(.bottom, 16)

                Divider().overlay(Palette.line)

                ScrollView {
                    VStack(alignment: .leading, spacing: 4) {
                        ForEach(AppPage.allCases) { item in
                            let isSelected = (page == item)
                            Button { page = item } label: {
                                HStack(spacing: 10) {
                                    Image(systemName: item.symbol).font(.system(size: 13, weight: .semibold))
                                        .foregroundStyle(isSelected ? Palette.green : Palette.muted).frame(width: 18)
                                    Text(item == .overview ? "Home (Overview)" : item.rawValue)
                                        .font(.system(size: 13, weight: isSelected ? .semibold : .medium))
                                        .foregroundStyle(isSelected ? Palette.ink : Palette.secondaryInk)
                                    Spacer()
                                    if item == .tests {
                                        Text(testBadgeText).font(.system(size: 10, weight: .bold, design: .monospaced))
                                            .foregroundStyle(testBadgeColor).padding(.horizontal, 7).padding(.vertical, 2)
                                            .background(testBadgeBg, in: Capsule())
                                    }
                                }
                                .padding(.horizontal, 12).padding(.vertical, 9)
                                .background(RoundedRectangle(cornerRadius: 9).fill(isSelected ? Palette.surfaceAlt : Color.clear))
                                .overlay(RoundedRectangle(cornerRadius: 9).stroke(isSelected ? Palette.green.opacity(0.45) : Color.clear, lineWidth: 1))
                            }.buttonStyle(.plain).pointingHand()
                        }
                    }.padding(12)
                }

                Divider().overlay(Palette.line)

                VStack(alignment: .leading, spacing: 10) {
                    Button { page = .tests; testRunner.runTests() } label: {
                        HStack(spacing: 8) {
                            if testRunner.isRunning { ProgressView().controlSize(.small) }
                            else { Image(systemName: "play.fill").font(.system(size: 10)) }
                            Text(testRunner.isRunning ? "Running tests…" : "Run All Tests").font(.system(size: 12.5, weight: .semibold))
                        }.frame(maxWidth: .infinity).padding(.vertical, 8)
                    }
                    .buttonStyle(.borderedProminent).tint(Palette.green).disabled(testRunner.isRunning).pointingHand(!testRunner.isRunning)

                    Button { page = .tests } label: {
                        VStack(alignment: .leading, spacing: 3) {
                            Text(testRunner.summaryLine.uppercased()).font(.system(size: 9.5, weight: .bold, design: .monospaced))
                                .foregroundStyle(testBadgeColor).lineLimit(1)
                            Text("Local viewer · no GPU inference on Mac").font(.system(size: 11)).foregroundStyle(Palette.muted)
                        }.frame(maxWidth: .infinity, alignment: .leading)
                    }.buttonStyle(.plain).pointingHand()
                }.padding(14).background(Palette.surface)
            }
            .frame(width: 244).background(Palette.sidebar)

            Rectangle().fill(Palette.line).frame(width: 1)

            VStack(spacing: 0) {
                HStack(spacing: 12) {
                    if page != .overview {
                        Button { page = .overview } label: {
                            HStack(spacing: 5) {
                                Image(systemName: "chevron.left").font(.system(size: 11, weight: .bold))
                                Text("Home").font(.system(size: 12.5, weight: .semibold))
                            }
                            .foregroundStyle(Palette.green).padding(.horizontal, 10).padding(.vertical, 5)
                            .background(Palette.paleGreen, in: RoundedRectangle(cornerRadius: 7))
                        }.buttonStyle(.plain).pointingHand()
                    }
                    Text(page == .overview ? "FactIndic · Home" : page.rawValue).font(.system(size: 13, weight: .semibold)).foregroundStyle(Palette.secondaryInk)
                    Spacer()
                    Button { page = .tests; testRunner.runTests() } label: {
                        HStack(spacing: 6) {
                            Image(systemName: "checkmark.seal.fill").font(.system(size: 11))
                            Text(testRunner.isRunning ? "Running…" : "Run Tests (\(testBadgeText))").font(.system(size: 12, weight: .medium))
                        }
                        .foregroundStyle(Palette.ink).padding(.horizontal, 10).padding(.vertical, 5)
                        .background(Palette.surfaceAlt, in: RoundedRectangle(cornerRadius: 7))
                        .overlay(RoundedRectangle(cornerRadius: 7).stroke(Palette.line, lineWidth: 1))
                    }.buttonStyle(.plain).disabled(testRunner.isRunning).pointingHand(!testRunner.isRunning)
                }
                .padding(.horizontal, 24).frame(height: 48).background(Palette.sidebar)

                Rectangle().fill(Palette.line).frame(height: 1)

                Group {
                    switch page {
                    case .overview: OverviewPage(testRunner: testRunner, navigate: { page = $0 })
                    case .baselines: BaselinePage(repoPath: testRunner.repoPath)
                    case .results: ResultsPage(navigateToGeneration: { page = .generation })
                    case .generation: GenerationMetricsPage()
                    case .liveDemo: LiveDemoPage()
                    case .tests: TestsPage(runner: testRunner)
                    case .method: MethodPage(repoPath: testRunner.repoPath)
                    }
                }.frame(maxWidth: .infinity, maxHeight: .infinity).background(Palette.background)
            }
        }.tint(Palette.green)
    }

    private var testBadgeText: String {
        if testRunner.isRunning { return "…" }
        if let code = testRunner.lastExitCode { return code == 0 ? "\(testRunner.passedCount)" : "!" }
        return "49"
    }
    private var testBadgeColor: Color {
        if let code = testRunner.lastExitCode { return code == 0 ? Palette.green : Palette.red }
        return Palette.blue
    }
    private var testBadgeBg: Color {
        if let code = testRunner.lastExitCode { return code == 0 ? Palette.paleGreen : Palette.paleRed }
        return Palette.paleBlue
    }
}

private struct OverviewPage: View {
    @ObservedObject var testRunner: TestRunner
    let navigate: (AppPage) -> Void

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                HStack {
                    HeaderTag(text: "EXPLORATORY PILOT · COMPLETE · \(testCountTag)")
                    Spacer()
                    Button {
                        NSWorkspace.shared.open(URL(fileURLWithPath: (testRunner.repoPath as NSString).appendingPathComponent("docs/final_submission")))
                    } label: { Label("Open Submissions Folder", systemImage: "folder").font(.system(size: 12, weight: .medium)) }
                    .buttonStyle(.bordered).pointingHand()
                }
                VStack(alignment: .leading, spacing: 10) {
                    Text("FactIndic").font(.system(size: 38, weight: .bold, design: .rounded)).tracking(-1.2).foregroundStyle(Palette.ink)
                    Text("Factuality-aware summarization for Hindi and Roman-script Hinglish").font(.system(size: 19, weight: .semibold)).foregroundStyle(Palette.green)
                    Text("Paired 500-article Hindi baseline, 120-summary Roman-script Hinglish LLM pilot, and live Colab T4 verification pipeline.")
                        .font(.system(size: 14)).foregroundStyle(Palette.secondaryInk).lineSpacing(4).frame(maxWidth: 760, alignment: .leading)
                }
                NoticeCard(title: "AI-screened results · human verification skipped",
                           message: "The 120-summary factuality labels came from one AI-assisted source comparison, and the live Colab demo uses Qwen3 + secondary mDeBERTa NLI. Treat them as exploratory screening, not human-verified evidence.",
                           tone: .amber)
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())], spacing: 14) {
                    MetricCard(value: "500", title: "Hindi articles", detail: "Paired XL-Sum vs. p100 baseline", accent: Palette.green, actionHint: "Baselines", action: { navigate(.baselines) })
                    MetricCard(value: "120", title: "Hinglish summaries", detail: "30 sources × 2 models × 2 prompts", accent: Palette.amber, actionHint: "Pilot", action: { navigate(.results) })
                    MetricCard(value: testRunner.lastExitCode == nil ? "49" : "\(testRunner.passedCount)",
                               title: testRunner.isRunning ? "Running tests…" : "Unit tests", detail: testRunner.summaryLine,
                               accent: testRunner.failedCount > 0 ? Palette.red : Palette.green, actionHint: "Run & View",
                               action: { navigate(.tests); if testRunner.cases.isEmpty { testRunner.runTests() } })
                    MetricCard(value: "0", title: "Local GPU load", detail: "Inference runs on Colab T4", accent: Palette.blue, actionHint: "Live JSON", action: { navigate(.liveDemo) })
                }
                VStack(alignment: .leading, spacing: 14) {
                    HStack(spacing: 10) {
                        Text("Quick actions").font(.system(size: 17, weight: .semibold)).foregroundStyle(Palette.ink)
                        Spacer()
                        Button("Hindi baselines") { navigate(.baselines) }.buttonStyle(.bordered).pointingHand()
                        Button("Pilot results") { navigate(.results) }.buttonStyle(.bordered).pointingHand()
                        Button("Run 49 Tests") { navigate(.tests); testRunner.runTests() }.buttonStyle(.bordered).pointingHand()
                        Button("Live demo & JSON") { navigate(.liveDemo) }.buttonStyle(.borderedProminent).tint(Palette.green).pointingHand()
                    }
                    Text("AI-assessed error counts ranged from 76.7% to 93.3% across the four Hinglish conditions. Both paired bootstrap intervals include zero (−6.7 pp for 1.7B, −3.3 pp for 4B), so this pilot does not identify a winning prompt.")
                        .font(.system(size: 13)).foregroundStyle(Palette.secondaryInk).lineSpacing(4)
                }
                .padding(18).background(Palette.surface, in: RoundedRectangle(cornerRadius: 15))
                .overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1))
                Text("The Hinglish translations in News_Hinglish_English were machine-generated and curated from English news articles. The corpus has no gold summaries, so ROUGE was not calculated.")
                    .font(.system(size: 12)).foregroundStyle(Palette.muted).padding(.horizontal, 2)
            }.padding(30).frame(maxWidth: 1040, alignment: .leading)
        }
    }

    private var testCountTag: String {
        if let code = testRunner.lastExitCode { return code == 0 ? "\(testRunner.passedCount) TESTS PASSED" : "\(testRunner.failedCount) TESTS FAILED" }
        return "49 UNIT TESTS"
    }
}

private struct BaselinePage: View {
    let repoPath: String
    @State private var selectedMetric: Int? = 0
    private let rows: [(name: String, hindi: String, p100: String, diff: String, ci: String, note: String)] = [
        ("ROUGE-1 F1", "37.24", "35.53", "−1.71 pp", "[−2.47, −0.96]", "Unigram overlap dropped 1.71 points under p100 mixing; 95% bootstrap CI excludes zero."),
        ("ROUGE-2 F1", "16.79", "15.24", "−1.55 pp", "[−2.28, −0.84]", "Bigram overlap dropped 1.55 points as English lexical insertions broke Hindi phrase continuity."),
        ("ROUGE-L F1", "31.20", "29.82", "−1.38 pp", "[−2.07, −0.69]", "Longest common subsequence dropped 1.38 points across the 500 matched XL-Sum test pairs.")
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HStack {
                    HeaderTag(text: "500 MATCHED HINDI TEST ARTICLES")
                    Spacer()
                    Button { NSWorkspace.shared.open(URL(fileURLWithPath: (repoPath as NSString).appendingPathComponent("results/paired_baseline_comparison.md"))) } label: {
                        Label("Open Baseline Report", systemImage: "doc.text").font(.system(size: 12, weight: .medium))
                    }.buttonStyle(.bordered).pointingHand()
                }
                Text("Hindi baselines").font(.system(size: 34, weight: .bold, design: .rounded)).tracking(-1).foregroundStyle(Palette.ink)
                Text("The same mT5 XL-Sum model summarized the original Hindi articles and a synthetic p100 code-mixed version. Both outputs use the same Hindi references. Click any metric row to inspect details.")
                    .font(.system(size: 13.5)).foregroundStyle(Palette.secondaryInk).lineSpacing(4).frame(maxWidth: 780, alignment: .leading)
                HStack(spacing: 14) {
                    MetricCard(value: "500", title: "Matched articles", detail: "Same article IDs in both conditions", accent: Palette.green)
                    MetricCard(value: "1.86 s", title: "Hindi inference", detail: "Mean time per document", accent: Palette.blue)
                    MetricCard(value: "1.90 s", title: "p100 inference", detail: "Mean time per document", accent: Palette.amber)
                }
                VStack(spacing: 0) {
                    HStack {
                        Text("METRIC"); Spacer()
                        Text("HINDI").frame(width: 85, alignment: .trailing)
                        Text("SYNTHETIC P100").frame(width: 125, alignment: .trailing)
                        Text("PAIRED CHANGE").frame(width: 115, alignment: .trailing)
                        Text("95% BOOTSTRAP CI").frame(width: 145, alignment: .trailing)
                    }.font(.system(size: 10, weight: .bold, design: .monospaced)).tracking(0.5).foregroundStyle(Palette.muted).padding(15).background(Palette.surfaceAlt)
                    ForEach(Array(rows.enumerated()), id: \.offset) { index, row in
                        let isSelected = selectedMetric == index
                        Button { selectedMetric = (selectedMetric == index ? nil : index) } label: {
                            VStack(alignment: .leading, spacing: 8) {
                                HStack {
                                    HStack(spacing: 8) {
                                        Image(systemName: isSelected ? "chevron.down" : "chevron.right").font(.system(size: 10, weight: .bold)).foregroundStyle(Palette.green)
                                        Text(row.name).font(.system(size: 13, weight: .semibold)).foregroundStyle(Palette.ink)
                                    }
                                    Spacer()
                                    Text(row.hindi).foregroundStyle(Palette.green).frame(width: 85, alignment: .trailing)
                                    Text(row.p100).foregroundStyle(Palette.blue).frame(width: 125, alignment: .trailing)
                                    Text(row.diff).fontWeight(.semibold).foregroundStyle(Palette.red).frame(width: 115, alignment: .trailing)
                                    Text(row.ci).foregroundStyle(Palette.secondaryInk).frame(width: 145, alignment: .trailing)
                                }.font(.system(size: 12.5, design: .monospaced))
                                if isSelected { Text(row.note).font(.system(size: 12)).foregroundStyle(Palette.secondaryInk).padding(.leading, 18) }
                            }.padding(.horizontal, 15).padding(.vertical, 14).background(isSelected ? Palette.hoverFill : Palette.surface)
                        }.buttonStyle(.plain).pointingHand()
                        if index < rows.count - 1 { Divider().overlay(Palette.line).padding(.horizontal, 15) }
                    }
                }.background(Palette.surface, in: RoundedRectangle(cornerRadius: 15)).overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1)).clipShape(RoundedRectangle(cornerRadius: 15))
                NoticeCard(title: "Lexical overlap fell under synthetic mixing",
                           message: "Paired bootstrap intervals (5,000 resamples, seed 42) excluded zero for all three ROUGE F1 changes. This measures overlap with Hindi references; it does not measure factuality or predict performance on naturally authored Hinglish.",
                           tone: .amber)
                Text("Truncation status matched for 491 of 500 pairs. The Hindi run marked 364 inputs truncated and the p100 run marked 355. Both used a 512-token source limit.")
                    .font(.system(size: 12)).foregroundStyle(Palette.muted).lineSpacing(4)
            }.padding(30).frame(maxWidth: 1000, alignment: .leading)
        }
    }
}

private struct ResultsPage: View {
    let navigateToGeneration: () -> Void
    @State private var selectedModel = "All models"
    @State private var selectedPrompt = "Both prompts"
    @State private var selectedRowId: String?
    private let models = ["All models", "Qwen3 · 1.7B", "Qwen3 · 4B"]
    private let prompts = ["Both prompts", "Standard", "Factuality-aware"]
    private var filtered: [PilotResult] {
        PilotResult.all.filter { (selectedModel == "All models" || $0.model == selectedModel) && (selectedPrompt == "Both prompts" || $0.prompt == selectedPrompt) }
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "AI-ASSISTED SCREENING · N = 30 PER CONDITION")
                Text("Pilot results").font(.system(size: 34, weight: .bold, design: .rounded)).tracking(-1).foregroundStyle(Palette.ink)
                Text("Error rate combines AI labels marked minor and major. Filter by model/prompt or click any row for condition notes.")
                    .font(.system(size: 13.5)).foregroundStyle(Palette.secondaryInk)
                HStack(spacing: 16) {
                    FilterPicker(title: "Model", selection: $selectedModel, options: models)
                    FilterPicker(title: "Prompt", selection: $selectedPrompt, options: prompts)
                    if selectedModel != "All models" || selectedPrompt != "Both prompts" {
                        Button("Reset") { selectedModel = "All models"; selectedPrompt = "Both prompts" }.buttonStyle(.bordered).controlSize(.small).pointingHand()
                    }
                    Spacer()
                    HStack(spacing: 12) {
                        LegendDot(color: Palette.green, label: "Supported")
                        LegendDot(color: Palette.amber, label: "Minor")
                        LegendDot(color: Palette.red, label: "Major")
                    }
                }
                VStack(spacing: 0) {
                    HStack {
                        Text("MODEL / PROMPT"); Spacer()
                        Text("SUPPORTED · MINOR · MAJOR").frame(width: 210, alignment: .trailing)
                        Text("BREAKDOWN").frame(width: 140, alignment: .center)
                        Text("ERROR RATE").frame(width: 95, alignment: .trailing)
                    }.font(.system(size: 10, weight: .bold, design: .monospaced)).tracking(0.6).foregroundStyle(Palette.muted).padding(15).background(Palette.surfaceAlt)
                    ForEach(filtered) { result in
                        ResultRow(result: result, isExpanded: selectedRowId == result.id,
                                  onTap: { selectedRowId = (selectedRowId == result.id ? nil : result.id) },
                                  onOpenGeneration: navigateToGeneration)
                        if result.id != filtered.last?.id { Divider().overlay(Palette.line).padding(.horizontal, 15) }
                    }
                }.background(Palette.surface, in: RoundedRectangle(cornerRadius: 15)).overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1)).clipShape(RoundedRectangle(cornerRadius: 15))
                HStack(spacing: 14) {
                    MetricCard(value: "−6.7 pp", title: "Qwen3 1.7B prompt diff", detail: "95% paired CI: −20.0 to +6.7 (includes 0)", accent: Palette.amber, actionHint: "Filter 1.7B", action: { selectedModel = "Qwen3 · 1.7B" })
                    MetricCard(value: "−3.3 pp", title: "Qwen3 4B prompt diff", detail: "95% paired CI: −13.3 to +6.7 (includes 0)", accent: Palette.amber, actionHint: "Filter 4B", action: { selectedModel = "Qwen3 · 4B" })
                }
                NoticeCard(title: "No prompt winner established", message: "Both paired bootstrap intervals include zero. Labels are AI judgments and have not been verified by a human annotator.", tone: .amber)
            }.padding(30).frame(maxWidth: 1000, alignment: .leading)
        }
    }
}

private struct LegendDot: View {
    let color: Color; let label: String
    var body: some View {
        HStack(spacing: 5) {
            Circle().fill(color).frame(width: 9, height: 9)
            Text(label).font(.system(size: 11.5, weight: .medium)).foregroundStyle(Palette.secondaryInk)
        }
    }
}

private struct FilterPicker: View {
    let title: String; @Binding var selection: String; let options: [String]
    var body: some View {
        Picker(title, selection: $selection) { ForEach(options, id: \.self) { Text($0).tag($0) } }
            .pickerStyle(.menu).frame(minWidth: 175, alignment: .leading).pointingHand()
    }
}

private struct ResultRow: View {
    let result: PilotResult; let isExpanded: Bool; let onTap: () -> Void; let onOpenGeneration: () -> Void
    var body: some View {
        Button(action: onTap) {
            VStack(alignment: .leading, spacing: 10) {
                HStack(spacing: 14) {
                    Image(systemName: isExpanded ? "chevron.down" : "chevron.right").font(.system(size: 10, weight: .bold)).foregroundStyle(Palette.green)
                    VStack(alignment: .leading, spacing: 3) {
                        Text(result.model).font(.system(size: 13.5, weight: .semibold)).foregroundStyle(Palette.ink)
                        Text(result.prompt).font(.system(size: 11.5)).foregroundStyle(Palette.muted)
                    }
                    Spacer()
                    Text("\(result.supported) · \(result.minor) · \(result.major)").font(.system(size: 12.5, design: .monospaced)).foregroundStyle(Palette.secondaryInk).frame(width: 210, alignment: .trailing)
                    GeometryReader { proxy in
                        let total = max(Double(result.supported + result.minor + result.major), 1.0)
                        HStack(spacing: 1) {
                            Rectangle().fill(Palette.green).frame(width: proxy.size.width * (Double(result.supported) / total))
                            Rectangle().fill(Palette.amber).frame(width: proxy.size.width * (Double(result.minor) / total))
                            Rectangle().fill(Palette.red).frame(width: proxy.size.width * (Double(result.major) / total))
                        }.clipShape(Capsule())
                    }.frame(width: 140, height: 10)
                    Text(result.rate.formatted(.percent.precision(.fractionLength(1)))).font(.system(size: 13.5, weight: .bold, design: .rounded)).foregroundStyle(Palette.red).frame(width: 95, alignment: .trailing)
                }
                if isExpanded {
                    HStack(alignment: .center) {
                        Text(result.notes).font(.system(size: 12)).foregroundStyle(Palette.secondaryInk).lineSpacing(3)
                        Spacer()
                        Button("Generation metrics →") { onOpenGeneration() }.buttonStyle(.bordered).controlSize(.small).pointingHand()
                    }.padding(.leading, 18)
                }
            }.padding(.horizontal, 15).padding(.vertical, 14).background(isExpanded ? Palette.hoverFill : Palette.surface)
        }.buttonStyle(.plain).pointingHand()
    }
}

private struct GenerationMetricsPage: View {
    private let columns: [(String, CGFloat)] = [
        ("MODEL", 140), ("PROMPT", 165), ("MEAN WORDS", 110), ("MEAN COMPRESSION", 145), ("CORPUS COMPRESSION", 150), ("MEAN SECONDS", 120)
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "FINAL COLAB RUN · 30 OUTPUTS PER CONDITION")
                Text("Generation metrics").font(.system(size: 34, weight: .bold, design: .rounded)).tracking(-1).foregroundStyle(Palette.ink)
                Text("Descriptive length, compression, and timing from the completed 120-summary run. Each condition used the same 30 source articles.")
                    .font(.system(size: 13.5)).foregroundStyle(Palette.secondaryInk).lineSpacing(4).frame(maxWidth: 760, alignment: .leading)
                ScrollView(.horizontal) {
                    VStack(spacing: 0) {
                        HStack(spacing: 12) {
                            ForEach(columns, id: \.0) { title, width in
                                Text(title).font(.system(size: 10, weight: .bold, design: .monospaced)).tracking(0.4).foregroundStyle(Palette.muted)
                                    .frame(width: width, alignment: title == "MODEL" || title == "PROMPT" ? .leading : .trailing)
                            }
                        }.padding(15).background(Palette.surfaceAlt)
                        ForEach(GenerationCondition.all) { row in
                            HStack(spacing: 12) {
                                Text(row.model).fontWeight(.semibold).foregroundStyle(Palette.ink).frame(width: columns[0].1, alignment: .leading)
                                Text(row.prompt).foregroundStyle(Palette.green).frame(width: columns[1].1, alignment: .leading)
                                Text(row.meanWords).foregroundStyle(Palette.secondaryInk).frame(width: columns[2].1, alignment: .trailing)
                                Text(row.meanCompression).foregroundStyle(Palette.blue).frame(width: columns[3].1, alignment: .trailing)
                                Text(row.corpusCompression).foregroundStyle(Palette.blue).frame(width: columns[4].1, alignment: .trailing)
                                Text(row.meanSeconds).foregroundStyle(Palette.amber).frame(width: columns[5].1, alignment: .trailing)
                            }.font(.system(size: 12.5, design: .monospaced)).padding(.horizontal, 15).padding(.vertical, 14)
                            if row.id != GenerationCondition.all.last?.id { Divider().overlay(Palette.line).padding(.horizontal, 15) }
                        }
                    }.frame(minWidth: columns.map(\.1).reduce(0, +) + 72, alignment: .leading)
                    .background(Palette.surface, in: RoundedRectangle(cornerRadius: 15))
                    .overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1)).clipShape(RoundedRectangle(cornerRadius: 15))
                }.scrollIndicators(.visible)
                Text("Compression is summary words divided by source words. Generation time is per output on a shared Colab Tesla T4 and is descriptive, not a model-quality score.")
                    .font(.system(size: 12)).foregroundStyle(Palette.muted).lineSpacing(4)
                VStack(alignment: .leading, spacing: 13) {
                    Text("Mechanical quality audit").font(.system(size: 17, weight: .semibold)).foregroundStyle(Palette.ink)
                    HStack(spacing: 12) {
                        MetricCard(value: "0", title: "Token-cap hits", detail: "All outputs ended below the retry cap")
                        MetricCard(value: "0", title: "Empty outputs", detail: "Every generation contains text")
                        MetricCard(value: "0", title: "Truncated sources", detail: "All selected inputs fit the source budget")
                        MetricCard(value: "2", title: "No final punctuation", detail: "Check these for completeness", accent: Palette.amber)
                    }
                }
                NoticeCard(title: "The audit does not verify factuality",
                           message: "The corpus has no gold summaries, so ROUGE is not applicable. Human factuality review was skipped. The AI-assisted labels remain unvalidated screening results.",
                           tone: .amber)
            }.padding(30).frame(maxWidth: 1080, alignment: .leading)
        }
    }
}

private struct LiveDemoPage: View {
    @State private var loadedReport: InteractiveRunReport?
    @State private var loadedFileName: String?
    @State private var loadError: String?
    @State private var copiedId: String?
    @State private var expandedSampleId: String? = "numbers"
    private let colabURL = URL(string: "https://colab.research.google.com/github/Sirohi0/factindic/blob/main/factindic_interactive_evaluation_colab.ipynb")!

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "INTERACTIVE COLAB T4 PIPELINE & JSON INSPECTOR")
                HStack(alignment: .center, spacing: 10) {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Live demo & JSON").font(.system(size: 34, weight: .bold, design: .rounded)).tracking(-1).foregroundStyle(Palette.ink)
                        Text("Inspect an exported Colab JSON report offline, preview a sample report, or copy challenge passages.")
                            .font(.system(size: 13.5)).foregroundStyle(Palette.secondaryInk)
                    }
                    Spacer()
                    Button("Load Sample") { loadedReport = InteractiveRunReport.sample; loadedFileName = "sample_qwen3_4b_transit.json"; loadError = nil }.buttonStyle(.bordered).pointingHand()
                    Button("Open Colab Demo") { NSWorkspace.shared.open(colabURL) }.buttonStyle(.bordered).pointingHand()
                    Button("Load JSON Result…") { openJSONFile() }.buttonStyle(.borderedProminent).tint(Palette.green).pointingHand()
                }
                if let error = loadError { NoticeCard(title: "Could not load JSON", message: error, tone: .red) }
                if let report = loadedReport {
                    VStack(alignment: .leading, spacing: 14) {
                        HStack {
                            Text(loadedFileName ?? "Loaded report").font(.system(size: 14, weight: .semibold)).foregroundStyle(Palette.ink)
                            Spacer()
                            Text(report.summary_review_status ?? "unknown").font(.system(size: 11, weight: .bold, design: .monospaced))
                                .foregroundStyle(report.summary_requires_manual_review == true ? Palette.amber : Palette.green)
                                .padding(.horizontal, 10).padding(.vertical, 5)
                                .background((report.summary_requires_manual_review == true ? Palette.paleAmber : Palette.paleGreen), in: Capsule())
                            Button("Clear") { loadedReport = nil; loadedFileName = nil }.buttonStyle(.bordered).controlSize(.small).pointingHand()
                        }
                        if let model = report.model, let prompt = report.prompt { Text("\(model) · \(prompt)").font(.system(size: 11.5, design: .monospaced)).foregroundStyle(Palette.blue) }
                        Text(report.summary).font(.system(size: 14)).foregroundStyle(Palette.ink).lineSpacing(4).textSelection(.enabled)
                        if let status = report.factuality_status { Text("Status: \(status)").font(.system(size: 12, weight: .medium)).foregroundStyle(Palette.green) }
                        if let claims = report.claims, !claims.isEmpty {
                            Divider().overlay(Palette.line)
                            ForEach(claims) { item in
                                VStack(alignment: .leading, spacing: 5) {
                                    HStack {
                                        Text(item.claim).font(.system(size: 12.5, weight: .semibold)).foregroundStyle(Palette.ink)
                                        Spacer()
                                        Text(item.assessment.uppercased()).font(.system(size: 10, weight: .bold, design: .monospaced))
                                            .foregroundStyle(item.assessment == "supported" ? Palette.green : Palette.amber)
                                            .padding(.horizontal, 8).padding(.vertical, 3)
                                            .background(item.assessment == "supported" ? Palette.paleGreen : Palette.paleAmber, in: Capsule())
                                    }
                                    if let quote = item.source_evidence, !quote.isEmpty {
                                        Text("Quote (\(item.quote_found_in_model_input == true ? "verified" : "unverified")): \"\(quote)\"").font(.system(size: 11.5)).foregroundStyle(Palette.secondaryInk)
                                    }
                                    if let nli = item.independent_nli_label {
                                        let scoreStr = item.independent_nli_score.map { String(format: "%.3f", $0) } ?? "—"
                                        Text("Secondary NLI (mDeBERTa): \(nli) (\(scoreStr))").font(.system(size: 10.5, design: .monospaced))
                                            .foregroundStyle(nli == "contradiction" ? Palette.red : Palette.muted)
                                    }
                                }.padding(.vertical, 5)
                            }
                        }
                    }.padding(18).background(Palette.surface, in: RoundedRectangle(cornerRadius: 15)).overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1))
                }
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Text("Live Colab T4 challenge suite (5 passages)").font(.system(size: 17, weight: .semibold)).foregroundStyle(Palette.ink)
                        Spacer()
                        Button(copiedId == "all" ? "Copied All 5" : "Copy All 5") {
                            let allText = ChallengeSample.all.map { "\($0.title)\n\($0.source)" }.joined(separator: "\n\n")
                            NSPasteboard.general.clearContents(); NSPasteboard.general.setString(allText, forType: .string); copiedId = "all"
                        }.buttonStyle(.bordered).controlSize(.small).pointingHand()
                    }
                    ForEach(ChallengeSample.all) { sample in
                        let isExpanded = expandedSampleId == sample.id
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Button { expandedSampleId = (isExpanded ? nil : sample.id) } label: {
                                    HStack(spacing: 8) {
                                        Image(systemName: isExpanded ? "chevron.down" : "chevron.right").font(.system(size: 10, weight: .bold)).foregroundStyle(Palette.green)
                                        Text(sample.title).font(.system(size: 14, weight: .semibold)).foregroundStyle(Palette.ink)
                                    }
                                }.buttonStyle(.plain).pointingHand()
                                Spacer()
                                Button(copiedId == sample.id ? "Copied" : "Copy Hinglish") {
                                    NSPasteboard.general.clearContents(); NSPasteboard.general.setString(sample.source, forType: .string); copiedId = sample.id
                                }.buttonStyle(.bordered).controlSize(.small).pointingHand()
                            }
                            Text(sample.source).font(.system(size: 12.5)).foregroundStyle(Palette.secondaryInk).lineSpacing(3).textSelection(.enabled)
                            if isExpanded {
                                HStack(spacing: 16) {
                                    Text("1.7B: \(sample.qwen17)").foregroundStyle(Palette.amber)
                                    Text("4B: \(sample.qwen4)").foregroundStyle(Palette.green)
                                    Text("NLI: \(sample.nliNote)").foregroundStyle(Palette.blue)
                                }.font(.system(size: 11, design: .monospaced)).padding(.top, 2)
                            }
                        }.padding(15).background(Palette.surface, in: RoundedRectangle(cornerRadius: 13))
                        .overlay(RoundedRectangle(cornerRadius: 13).stroke(isExpanded ? Palette.green.opacity(0.55) : Palette.line, lineWidth: 1))
                    }
                }
            }.padding(30).frame(maxWidth: 1040, alignment: .leading)
        }
    }

    private func openJSONFile() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.json]; panel.allowsMultipleSelection = false; panel.canChooseDirectories = false
        guard panel.runModal() == .OK, let url = panel.url else { return }
        do { loadedReport = try JSONDecoder().decode(InteractiveRunReport.self, from: Data(contentsOf: url)); loadedFileName = url.lastPathComponent; loadError = nil }
        catch { loadError = error.localizedDescription }
    }
}

private struct TestsPage: View {
    @ObservedObject var runner: TestRunner
    @State private var selectedFile = "All files"
    @State private var searchText = ""
    @State private var showRawLog = false
    private let testFiles = ["All files", "test_analysis.py", "test_checks.py", "test_codemix.py", "test_interactive_notebook.py", "test_metrics.py", "test_runner.py", "test_text_utils.py"]
    private var filteredCases: [TestCaseResult] {
        runner.cases.filter { (selectedFile == "All files" || $0.file == selectedFile) && (searchText.isEmpty || $0.name.localizedCaseInsensitiveContains(searchText) || $0.file.localizedCaseInsensitiveContains(searchText)) }
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                HeaderTag(text: runner.isRunning ? "RUNNING PYTEST…" : runner.summaryLine.uppercased(),
                          tone: runner.failedCount > 0 ? Palette.red : Palette.green,
                          background: runner.failedCount > 0 ? Palette.paleRed : Palette.paleGreen)
                HStack(alignment: .center, spacing: 10) {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Test suite").font(.system(size: 34, weight: .bold, design: .rounded)).tracking(-1).foregroundStyle(Palette.ink)
                        Text("Runs Python unit & notebook contract checks locally in \(runner.repoPath) (no GPU or LLM inference).").font(.system(size: 13)).foregroundStyle(Palette.muted)
                    }
                    Spacer()
                    Button("Choose Repo…") { runner.chooseRepoFolder() }.buttonStyle(.bordered).pointingHand()
                    Button("Verify Setup") { runner.runVerifySetup() }.buttonStyle(.bordered).disabled(runner.isRunning).pointingHand(!runner.isRunning)
                    Button { runner.runTests(target: selectedFile == "All files" ? "tests" : "tests/\(selectedFile)") } label: {
                        HStack(spacing: 6) {
                            if runner.isRunning { ProgressView().controlSize(.small) }
                            Text(runner.isRunning ? "Running…" : (selectedFile == "All files" ? "Run All Tests" : "Run \(selectedFile)"))
                        }
                    }.buttonStyle(.borderedProminent).tint(Palette.green).disabled(runner.isRunning).pointingHand(!runner.isRunning)
                }
                HStack(spacing: 14) {
                    MetricCard(value: runner.cases.isEmpty ? "49" : "\(runner.passedCount)", title: "Passed", detail: runner.cases.isEmpty ? "Expected test count" : "Verified in latest run", accent: Palette.green)
                    MetricCard(value: "\(runner.failedCount)", title: "Failed", detail: runner.failedCount == 0 ? "Zero failures" : "Inspect raw output below", accent: runner.failedCount == 0 ? Palette.green : Palette.red)
                    MetricCard(value: runner.durationText ?? "—", title: "Duration", detail: "Runs via .venv/bin/python", accent: Palette.blue)
                }
                HStack(spacing: 12) {
                    Picker("File", selection: $selectedFile) { ForEach(testFiles, id: \.self) { Text($0).tag($0) } }.pickerStyle(.menu).frame(width: 240, alignment: .leading).pointingHand()
                    TextField("Filter test cases…", text: $searchText).textFieldStyle(.roundedBorder).frame(maxWidth: 280)
                    Spacer()
                    Toggle("Show Raw Output", isOn: $showRawLog).toggleStyle(.switch).font(.system(size: 12.5, weight: .medium)).foregroundStyle(Palette.ink).pointingHand()
                }
                if showRawLog || (runner.cases.isEmpty && !runner.rawOutput.isEmpty) {
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text("Console output").font(.system(size: 13, weight: .semibold)).foregroundStyle(Palette.ink)
                            Spacer()
                            Button("Copy Output") { NSPasteboard.general.clearContents(); NSPasteboard.general.setString(runner.rawOutput, forType: .string) }.buttonStyle(.bordered).controlSize(.small).pointingHand()
                        }
                        ScrollView {
                            Text(runner.rawOutput.isEmpty ? "No output yet. Click Run All Tests." : runner.rawOutput)
                                .font(.system(size: 11.5, design: .monospaced)).foregroundStyle(Palette.secondaryInk).frame(maxWidth: .infinity, alignment: .leading).textSelection(.enabled)
                        }.frame(maxHeight: 240).padding(12).background(Palette.surfaceAlt, in: RoundedRectangle(cornerRadius: 10)).overlay(RoundedRectangle(cornerRadius: 10).stroke(Palette.line, lineWidth: 1))
                    }.padding(16).background(Palette.surface, in: RoundedRectangle(cornerRadius: 14)).overlay(RoundedRectangle(cornerRadius: 14).stroke(Palette.line, lineWidth: 1))
                }
                VStack(spacing: 0) {
                    HStack {
                        Text("TEST CASE"); Spacer()
                        Text("FILE").frame(width: 210, alignment: .leading)
                        Text("STATUS").frame(width: 90, alignment: .trailing)
                    }.font(.system(size: 10, weight: .bold, design: .monospaced)).tracking(0.6).foregroundStyle(Palette.muted).padding(15).background(Palette.surfaceAlt)
                    if filteredCases.isEmpty {
                        HStack { Text(runner.cases.isEmpty ? "Click 'Run All Tests' to execute pytest and inspect all 49 checks." : "No test cases match the current filter.").font(.system(size: 13)).foregroundStyle(Palette.muted); Spacer() }.padding(18)
                    } else {
                        ForEach(filteredCases) { item in
                            HStack(spacing: 12) {
                                Text(item.name).font(.system(size: 12, design: .monospaced)).foregroundStyle(Palette.ink).lineLimit(1)
                                Spacer()
                                Text(item.file).font(.system(size: 11.5, design: .monospaced)).foregroundStyle(Palette.muted).frame(width: 210, alignment: .leading)
                                Text(item.status.rawValue).font(.system(size: 10, weight: .bold, design: .monospaced))
                                    .foregroundStyle(item.status == .passed ? Palette.green : Palette.red)
                                    .padding(.horizontal, 8).padding(.vertical, 3)
                                    .background(item.status == .passed ? Palette.paleGreen : Palette.paleRed, in: Capsule())
                                    .frame(width: 90, alignment: .trailing)
                            }.padding(.horizontal, 15).padding(.vertical, 10)
                            if item.id != filteredCases.last?.id { Divider().overlay(Palette.line).padding(.horizontal, 15) }
                        }
                    }
                }.background(Palette.surface, in: RoundedRectangle(cornerRadius: 15)).overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1)).clipShape(RoundedRectangle(cornerRadius: 15))
            }.padding(30).frame(maxWidth: 1040, alignment: .leading)
        }
    }
}

private struct MethodPage: View {
    let repoPath: String
    private let references: [(String, String)] = [
        ("News_Hinglish_English Dataset", "https://huggingface.co/datasets/suyash2739/News_Hinglish_English"),
        ("XL-Sum Paper (ACL 2021)", "https://aclanthology.org/2021.findings-acl.413/"),
        ("mT5 Paper (NAACL 2021)", "https://aclanthology.org/2021.naacl-main.41/"),
        ("Qwen3 Technical Report (arXiv)", "https://arxiv.org/abs/2505.09388"),
        ("mDeBERTa-v3 NLI (Hugging Face)", "https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"),
        ("FactIndic GitHub Repository", "https://github.com/Sirohi0/factindic")
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "RESEARCH DESIGN")
                Text("Method & limits").font(.system(size: 34, weight: .bold, design: .rounded)).tracking(-1).foregroundStyle(Palette.ink)
                InfoBlock(title: "Target language", message: "Roman-script Hinglish: Hindi words written in Latin letters and mixed with English. The source corpus pairs English news articles with machine-generated and curated Hinglish translations.")
                InfoBlock(title: "Paired generation", message: "Thirty fixed source articles were summarized by Qwen3 1.7B and Qwen3 4B. Each model used a standard prompt and a factuality-aware prompt, producing 120 outputs total. Generation ran on a Colab Tesla T4.")
                InfoBlock(title: "Factuality screening", message: "One AI reviewer compared each summary to the Hinglish source visible to the model. The English article was a reading aid. The resulting 19 supported, 27 minor-error, and 74 major-error labels are provisional AI judgments, not human annotations.")
                InfoBlock(title: "Interactive Colab safeguards", message: "The live evaluation notebook uses pure greedy decoding (removing repetition_penalty=1.03 and no_repeat_ngram_size=3, which caused ±1 digit shifts), verifies evidence quotes verbatim, and adds MoritzLaurer/mDeBERTa-v3-base-mnli-xnli as an unvalidated secondary NLI signal.")
                InfoBlock(title: "Why no ROUGE", message: "This dataset does not contain gold summaries. Reference-overlap metrics would not be applicable to these generated outputs.")
                NoticeCard(title: "Scope of conclusions", message: "The sample is small, limited to news, and uses translated rather than naturally authored Hinglish. The pilot does not establish a winning prompt or generalize to all Hinglish. Human verification is intentionally skipped for this version.", tone: .amber)
                VStack(alignment: .leading, spacing: 10) {
                    Text("References & links").font(.system(size: 15, weight: .semibold)).foregroundStyle(Palette.ink)
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 10) {
                        ForEach(references, id: \.0) { title, urlString in
                            Button { if let url = URL(string: urlString) { NSWorkspace.shared.open(url) } } label: {
                                HStack {
                                    Text(title).font(.system(size: 12.5, weight: .medium)).foregroundStyle(Palette.blue)
                                    Spacer()
                                    Image(systemName: "arrow.up.right.square").font(.system(size: 12)).foregroundStyle(Palette.blue)
                                }.padding(12).background(Palette.surface, in: RoundedRectangle(cornerRadius: 10)).overlay(RoundedRectangle(cornerRadius: 10).stroke(Palette.line, lineWidth: 1))
                            }.buttonStyle(.plain).pointingHand()
                        }
                    }
                }
                Text("Dataset: suyash2739/News_Hinglish_English · revision 22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359 · Local repo: \(repoPath)")
                    .font(.system(size: 10.5, design: .monospaced)).foregroundStyle(Palette.muted).textSelection(.enabled)
            }.padding(30).frame(maxWidth: 920, alignment: .leading)
        }
    }
}

private struct InfoBlock: View {
    let title: String; let message: String
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title).font(.system(size: 15, weight: .semibold)).foregroundStyle(Palette.green)
            Text(message).font(.system(size: 13)).foregroundStyle(Palette.secondaryInk).lineSpacing(4).fixedSize(horizontal: false, vertical: true)
        }.frame(maxWidth: .infinity, alignment: .leading).padding(18).background(Palette.surface, in: RoundedRectangle(cornerRadius: 14)).overlay(RoundedRectangle(cornerRadius: 14).stroke(Palette.line, lineWidth: 1))
    }
}
