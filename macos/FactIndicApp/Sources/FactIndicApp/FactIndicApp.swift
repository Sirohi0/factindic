import SwiftUI

@main
struct FactIndicApp: App {
    var body: some Scene {
        WindowGroup {
            FactIndicWindow()
                .frame(minWidth: 900, minHeight: 650)
        }
        .windowStyle(.titleBar)
        .defaultSize(width: 1120, height: 780)
    }
}

private enum Palette {
    static let background = Color(red: 0.965, green: 0.961, blue: 0.941)
    static let surface = Color.white
    static let ink = Color(red: 0.09, green: 0.14, blue: 0.12)
    static let muted = Color(red: 0.39, green: 0.45, blue: 0.41)
    static let green = Color(red: 0.14, green: 0.40, blue: 0.31)
    static let paleGreen = Color(red: 0.90, green: 0.94, blue: 0.90)
    static let amber = Color(red: 0.54, green: 0.34, blue: 0.10)
    static let paleAmber = Color(red: 0.97, green: 0.94, blue: 0.86)
    static let line = Color(red: 0.86, green: 0.88, blue: 0.85)
}

private enum AppPage: String, CaseIterable, Identifiable {
    case overview = "Overview"
    case baselines = "Hindi baselines"
    case results = "Pilot results"
    case method = "Method & limits"

    var id: String { rawValue }

    var symbol: String {
        switch self {
        case .overview: "square.grid.2x2"
        case .baselines: "chart.xyaxis.line"
        case .results: "chart.bar.xaxis"
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

    var id: String { "\(model)-\(prompt)" }
    var errors: Int { minor + major }
    var rate: Double { Double(errors) / 30.0 }

    static let all: [PilotResult] = [
        .init(model: "Qwen3 · 1.7B", prompt: "Standard", supported: 2, minor: 4, major: 24),
        .init(model: "Qwen3 · 1.7B", prompt: "Factuality-aware", supported: 4, minor: 8, major: 18),
        .init(model: "Qwen3 · 4B", prompt: "Standard", supported: 6, minor: 9, major: 15),
        .init(model: "Qwen3 · 4B", prompt: "Factuality-aware", supported: 7, minor: 6, major: 17)
    ]
}

private struct MetricCard: View {
    let value: String
    let title: String
    let detail: String

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(value)
                .font(.system(size: 32, weight: .semibold, design: .rounded))
                .foregroundStyle(Palette.green)
            Text(title).font(.system(size: 13, weight: .semibold))
            Text(detail)
                .font(.system(size: 12))
                .foregroundStyle(Palette.muted)
                .fixedSize(horizontal: false, vertical: true)
        }
        .frame(maxWidth: .infinity, minHeight: 115, alignment: .leading)
        .padding(18)
        .background(Palette.surface, in: RoundedRectangle(cornerRadius: 15))
        .overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1))
    }
}

private struct FactIndicWindow: View {
    @State private var page: AppPage? = .overview

    var body: some View {
        NavigationSplitView {
            List(AppPage.allCases, selection: $page) { item in
                Label(item.rawValue, systemImage: item.symbol)
                    .tag(item as AppPage?)
            }
            .listStyle(.sidebar)
            .navigationTitle("FactIndic")
            .safeAreaInset(edge: .bottom) {
                VStack(alignment: .leading, spacing: 5) {
                    Text("LOCAL VIEWER")
                        .font(.system(size: 9, weight: .bold, design: .monospaced))
                        .tracking(1.1)
                    Text("No model runs on this Mac")
                        .font(.system(size: 11))
                        .foregroundStyle(Palette.muted)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(16)
            }
        } detail: {
            Group {
                switch page ?? .overview {
                case .overview: OverviewPage { page = .results }
                case .baselines: BaselinePage()
                case .results: ResultsPage()
                case .method: MethodPage()
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(Palette.background)
        }
        .tint(Palette.green)
    }
}

private struct BaselinePage: View {
    private let rows: [(String, String, String, String)] = [
        ("ROUGE-1 F1", "37.24", "33.97", "−1.71 pp"),
        ("ROUGE-2 F1", "16.79", "13.68", "−1.55 pp"),
        ("ROUGE-L F1", "31.20", "28.55", "−1.38 pp"),
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "500 MATCHED HINDI TEST ARTICLES")
                Text("Hindi baselines")
                    .font(.system(size: 34, weight: .bold, design: .rounded))
                    .tracking(-1)
                Text("The same mT5 XL-Sum model summarized the original Hindi articles and a synthetic p100 code-mixed version. Both outputs use the same Hindi references.")
                    .font(.system(size: 13))
                    .foregroundStyle(Palette.muted)
                    .lineSpacing(4)
                    .frame(maxWidth: 760, alignment: .leading)

                HStack(spacing: 14) {
                    MetricCard(value: "500", title: "Matched articles", detail: "Same article IDs in both conditions")
                    MetricCard(value: "1.86 s", title: "Hindi inference", detail: "Mean time per document")
                    MetricCard(value: "1.90 s", title: "p100 inference", detail: "Mean time per document")
                }

                VStack(spacing: 0) {
                    HStack {
                        Text("METRIC")
                        Spacer()
                        Text("HINDI").frame(width: 110, alignment: .trailing)
                        Text("SYNTHETIC P100").frame(width: 150, alignment: .trailing)
                        Text("PAIRED CHANGE").frame(width: 140, alignment: .trailing)
                    }
                    .font(.system(size: 9, weight: .bold, design: .monospaced))
                    .tracking(0.5)
                    .foregroundStyle(Palette.muted)
                    .padding(15)
                    ForEach(Array(rows.enumerated()), id: \.offset) { index, row in
                        HStack {
                            Text(row.0).font(.system(size: 13, weight: .semibold))
                            Spacer()
                            Text(row.1).frame(width: 110, alignment: .trailing)
                            Text(row.2).frame(width: 150, alignment: .trailing)
                            Text(row.3).frame(width: 140, alignment: .trailing)
                        }
                        .font(.system(size: 12, design: .monospaced))
                        .padding(.horizontal, 15)
                        .padding(.vertical, 14)
                        if index < rows.count - 1 { Divider().padding(.horizontal, 15) }
                    }
                }
                .background(Palette.surface, in: RoundedRectangle(cornerRadius: 15))
                .overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1))

                NoticeCard(
                    title: "Lexical overlap fell under synthetic mixing",
                    message: "Paired bootstrap intervals excluded zero for all three ROUGE F1 changes. This measures overlap with Hindi references; it does not measure factuality or predict performance on naturally authored Hinglish.",
                    tone: .amber
                )
                Text("Truncation status matched for 491 of 500 pairs. The Hindi run marked 364 inputs truncated and the p100 run marked 355. Both used a 512-token source limit.")
                    .font(.system(size: 12))
                    .foregroundStyle(Palette.muted)
                    .lineSpacing(4)
            }
            .padding(30)
            .frame(maxWidth: 980, alignment: .leading)
        }
    }
}

private struct OverviewPage: View {
    let showResults: () -> Void

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                HeaderTag(text: "EXPLORATORY PILOT · COMPLETE")
                VStack(alignment: .leading, spacing: 12) {
                    Text("FactIndic")
                        .font(.system(size: 39, weight: .bold, design: .rounded))
                        .tracking(-1.4)
                    Text("Factuality-aware summarization for Roman-script Hinglish")
                        .font(.system(size: 20, weight: .medium))
                        .foregroundStyle(Palette.green)
                    Text("A paired pilot compared two Qwen3 model sizes and two prompt styles on the same 30 Hinglish news sources.")
                        .font(.system(size: 14))
                        .foregroundStyle(Palette.muted)
                        .lineSpacing(4)
                        .frame(maxWidth: 720, alignment: .leading)
                }

                NoticeCard(
                    title: "AI-screened results · human verification skipped",
                    message: "The factuality labels shown here came from one AI-assisted source comparison. Treat them as exploratory screening, not human-verified evidence.",
                    tone: .amber
                )

                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())], spacing: 14) {
                    MetricCard(value: "30", title: "Hinglish sources", detail: "Same sources across all four conditions")
                    MetricCard(value: "120", title: "Generated summaries", detail: "Two model sizes × two prompt styles")
                    MetricCard(value: "4", title: "Experimental conditions", detail: "Greedy generation on a Colab T4 GPU")
                }

                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Text("Pilot snapshot").font(.system(size: 18, weight: .semibold))
                        Spacer()
                        Button("Explore results") { showResults() }
                            .buttonStyle(.borderedProminent)
                            .tint(Palette.green)
                    }
                    Text("AI-assessed error counts ranged from 76.7% to 93.3%. Paired bootstrap intervals include zero for both prompt comparisons, so this small pilot does not identify a winning prompt.")
                        .font(.system(size: 13))
                        .foregroundStyle(Palette.muted)
                        .lineSpacing(4)
                }
                .padding(19)
                .background(Palette.surface, in: RoundedRectangle(cornerRadius: 15))
                .overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1))

                Text("The Hinglish translations were machine-generated and curated from English news articles. The corpus has no gold summaries, so ROUGE was not calculated.")
                    .font(.system(size: 12))
                    .foregroundStyle(Palette.muted)
                    .padding(.horizontal, 2)
            }
            .padding(30)
            .frame(maxWidth: 980, alignment: .leading)
        }
    }
}

private struct ResultsPage: View {
    @State private var selectedModel = "All models"
    @State private var selectedPrompt = "Both prompts"

    private let models = ["All models", "Qwen3 · 1.7B", "Qwen3 · 4B"]
    private let prompts = ["Both prompts", "Standard", "Factuality-aware"]

    private var filtered: [PilotResult] {
        PilotResult.all.filter { result in
            (selectedModel == "All models" || result.model == selectedModel)
                && (selectedPrompt == "Both prompts" || result.prompt == selectedPrompt)
        }
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "AI-ASSISTED SCREENING · N = 30 PER CONDITION")
                Text("Pilot results")
                    .font(.system(size: 34, weight: .bold, design: .rounded))
                    .tracking(-1)
                Text("Error rate combines AI labels marked minor and major. Choose a model or prompt to filter the view.")
                    .font(.system(size: 13))
                    .foregroundStyle(Palette.muted)

                HStack(spacing: 20) {
                    FilterPicker(title: "Model", selection: $selectedModel, options: models)
                    FilterPicker(title: "Prompt", selection: $selectedPrompt, options: prompts)
                    Spacer()
                }

                VStack(spacing: 0) {
                    HStack {
                        Text("MODEL / PROMPT")
                        Spacer()
                        Text("SUPPORTED · MINOR · MAJOR")
                            .frame(width: 220, alignment: .trailing)
                        Text("ERROR RATE")
                            .frame(width: 115, alignment: .trailing)
                    }
                    .font(.system(size: 9, weight: .bold, design: .monospaced))
                    .tracking(0.6)
                    .foregroundStyle(Palette.muted)
                    .padding(15)
                    ForEach(filtered) { result in
                        ResultRow(result: result)
                        if result.id != filtered.last?.id { Divider().padding(.horizontal, 15) }
                    }
                }
                .background(Palette.surface, in: RoundedRectangle(cornerRadius: 15))
                .overlay(RoundedRectangle(cornerRadius: 15).stroke(Palette.line, lineWidth: 1))

                NoticeCard(
                    title: "No prompt winner established",
                    message: "Both paired bootstrap intervals include zero. Labels are AI judgments and have not been verified by a human annotator.",
                    tone: .amber
                )
            }
            .padding(30)
            .frame(maxWidth: 980, alignment: .leading)
        }
    }
}

private struct FilterPicker: View {
    let title: String
    @Binding var selection: String
    let options: [String]

    var body: some View {
        Picker(title, selection: $selection) {
            ForEach(options, id: \.self) { option in Text(option).tag(option) }
        }
        .pickerStyle(.menu)
        .frame(minWidth: 175, alignment: .leading)
    }
}

private struct ResultRow: View {
    let result: PilotResult

    var body: some View {
        HStack(spacing: 14) {
            VStack(alignment: .leading, spacing: 4) {
                Text(result.model).font(.system(size: 13, weight: .semibold))
                Text(result.prompt).font(.system(size: 11)).foregroundStyle(Palette.muted)
            }
            Spacer()
            Text("\(result.supported) · \(result.minor) · \(result.major)")
                .font(.system(size: 12, design: .monospaced))
                .frame(width: 220, alignment: .trailing)
            VStack(alignment: .trailing, spacing: 6) {
                Text(result.rate.formatted(.percent.precision(.fractionLength(1))))
                    .font(.system(size: 13, weight: .semibold, design: .rounded))
                GeometryReader { proxy in
                    ZStack(alignment: .leading) {
                        Capsule().fill(Palette.paleGreen)
                        Capsule().fill(Palette.green).frame(width: proxy.size.width * result.rate)
                    }
                }
                .frame(width: 92, height: 6)
            }
            .frame(width: 115, alignment: .trailing)
        }
        .padding(.horizontal, 15)
        .padding(.vertical, 14)
    }
}

private struct MethodPage: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HeaderTag(text: "RESEARCH DESIGN")
                Text("Method & limits")
                    .font(.system(size: 34, weight: .bold, design: .rounded))
                    .tracking(-1)
                InfoBlock(title: "Target language", message: "Roman-script Hinglish: Hindi words written in Latin letters and mixed with English. The source corpus pairs English news articles with machine-generated and curated Hinglish translations.")
                InfoBlock(title: "Paired generation", message: "Thirty fixed source articles were summarized by Qwen3 1.7B and Qwen3 4B. Each model used a standard prompt and a factuality-aware prompt, producing 120 outputs total. Generation ran on a Colab Tesla T4.")
                InfoBlock(title: "Factuality screening", message: "One AI reviewer compared each summary to the Hinglish source visible to the model. The English article was a reading aid. The resulting 19 supported, 27 minor-error, and 74 major-error labels are provisional AI judgments, not human annotations.")
                InfoBlock(title: "Why no ROUGE", message: "This dataset does not contain gold summaries. Reference-overlap metrics would not be applicable to these generated outputs.")
                NoticeCard(title: "Scope of conclusions", message: "The sample is small, limited to news, and uses translated rather than naturally authored Hinglish. The pilot does not establish a winning prompt or generalize to all Hinglish. Human verification is intentionally skipped for this version.", tone: .amber)
                Text("Dataset: suyash2739/News_Hinglish_English · revision 22a19b81fd8cc151a9d011cfdd7e6dd4e9f2b359")
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundStyle(Palette.muted)
                    .textSelection(.enabled)
            }
            .padding(30)
            .frame(maxWidth: 860, alignment: .leading)
        }
    }
}

private struct InfoBlock: View {
    let title: String
    let message: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title).font(.system(size: 15, weight: .semibold))
            Text(message)
                .font(.system(size: 13))
                .foregroundStyle(Palette.muted)
                .lineSpacing(4)
                .fixedSize(horizontal: false, vertical: true)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(18)
        .background(Palette.surface, in: RoundedRectangle(cornerRadius: 14))
        .overlay(RoundedRectangle(cornerRadius: 14).stroke(Palette.line, lineWidth: 1))
    }
}

private struct HeaderTag: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.system(size: 9, weight: .bold, design: .monospaced))
            .tracking(1)
            .foregroundStyle(Palette.green)
            .padding(.horizontal, 10)
            .padding(.vertical, 7)
            .background(Palette.paleGreen, in: Capsule())
    }
}

private struct NoticeCard: View {
    enum Tone { case amber }
    let title: String
    let message: String
    let tone: Tone

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: "info.circle.fill")
                .font(.system(size: 17))
                .foregroundStyle(Palette.amber)
                .padding(.top, 1)
            VStack(alignment: .leading, spacing: 5) {
                Text(title).font(.system(size: 13, weight: .semibold))
                Text(message)
                    .font(.system(size: 12))
                    .lineSpacing(3)
                    .foregroundStyle(Palette.muted)
                    .fixedSize(horizontal: false, vertical: true)
            }
            Spacer(minLength: 0)
        }
        .padding(15)
        .background(Palette.paleAmber, in: RoundedRectangle(cornerRadius: 13))
    }
}
