"""Reviewed bilingual explanation designs; no domain rules in the Markdown analyzer.

Each entry replaces only the named source section. Examples explicitly distinguish
illustrative assumptions from product guarantees. Canonical Markdown is untouched.
"""

def _unit(key, ko_title, en_title, ko, en):
    return {'key': key, 'title': {'ko': ko_title, 'en': en_title}, 'body': {'ko': ko, 'en': en}}


DESIGNS = {
 ('data-platform-flink', '5.5 Watermark'): {
  'id': 'watermark',
  'rationale': 'Separate event time, arrival order and estimated progress; make late-event policy and idleness limits visible.',
  'assumptions': 'Illustrative five-second out-of-order allowance; no universal Flink formula or window outcome is asserted.',
  'units': [
   _unit('purpose', 'Watermark — 결과를 언제 낼까?', 'Watermark — when can results be emitted?',
     'Watermark는 **이벤트 시각의 진행 기준**이다. 대부분의 이전 이벤트가 도착했다고 추정하여 결과를 언제 내고 상태를 얼마나 보관할지 판단한다.\n\n이벤트 시각은 사건이 발생한 시각이다. 도착 순서는 시스템이 데이터를 받은 순서다. 두 순서는 다를 수 있어, 늦은 이벤트가 없다는 보장으로 watermark를 사용하면 안 된다.',
     'A watermark is an **estimate of event-time progress**. It helps decide when to emit results and how long to retain state, assuming most earlier events have arrived.\n\nEvent time is when an event happened. Arrival order is the order in which the system receives events. These can differ: a watermark does not guarantee that no late events remain.'),
   _unit('timeline', 'Watermark — 도착 순서와 진행 기준', 'Watermark — arrival order and progress',
     '**원문 기반 수치 예시:** 최신 이벤트 시각 10:01:10, 순서 뒤바뀜 허용 5초를 가정하면 watermark ≈ 10:01:05다. 모든 구현에 적용되는 공식이 아니다.\n\n| 도착 순서 | 이벤트 시각 | 판단 |\n|---|---|---|\n| 먼저 관찰 | 10:01:10 | 예시의 최신 시각 |\n| 이후 도착 (설명용 입력) | 10:01:03 | 10:01:05보다 과거 → late event |\n\n**이벤트 시간축:** 10:01:03 → 10:01:05 (watermark) → 10:01:10. 도착은 이 시간축 순서와 다르다.',
     '**Source-based numerical example:** latest event time 10:01:10, assuming five seconds of out-of-order allowance, gives watermark ≈ 10:01:05. This is not a universal formula.\n\n| Arrival order | Event time | Interpretation |\n|---|---|---|\n| Observed first | 10:01:10 | Latest time in the example |\n| Arrives later (illustrative input) | 10:01:03 | Earlier than 10:01:05 → late event |\n\n**Event-time axis:** 10:01:03 → 10:01:05 (watermark) → 10:01:10. Arrival order differs from this time order.'),
   _unit('policy', 'Watermark — 늦은 이벤트와 비용', 'Watermark — late events and cost',
     '10:01:03 이벤트가 늦다는 판단과 **그 이벤트를 어떻게 처리할지**는 별개다. 원문의 선택지는 버리기, allowed lateness, 별도 처리다. 실제 window·연산자·정책을 확인하기 전에는 포함 또는 폐기를 단정하지 않는다.\n\n진행을 늦추면 결과 지연과 state 보관 비용이 늘 수 있다. 빠르게 진행하면 늦은 이벤트 누락 가능성이 커진다. 더 오래 기다려도 정확도가 자동 보장되지 않는다.',
     'Classifying the 10:01:03 event as late does not decide **how to handle it**. The source lists dropping it, allowed lateness, and separate handling. Do not assert inclusion or rejection without checking the actual window, operator, and policy.\n\nSlower progress may increase result latency and state retention cost. Faster progress may omit late events. Waiting longer does not automatically guarantee accuracy.'),
   _unit('idleness', 'Watermark — 입력이 멈춘 경우', 'Watermark — when an input becomes idle',
     '여러 입력의 진행은 보통 **가장 느린 활성 입력**에 묶인다. Idle partition이 진행을 막으면 idleness 설정을 확인한다.\n\n입력별 watermark → idle 여부 → late-event 정책을 함께 점검한다. Event-time session 종료는 단순한 wall-clock 대기로 결정되지 않는다.\n\n[Flink watermark 원문 근거](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/)',
     'Across multiple inputs, progress is generally limited by the **slowest active input**. An idle partition can hold progress back; check idleness settings.\n\nCheck per-input watermarks → idle status → late-event policy together. Event-time session completion is not determined by wall-clock waiting alone.\n\n[Flink watermark source](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/)')]},
 ('aws-cloud-networking', 'Security Group vs NACL'): {
  'id': 'sg-nacl', 'rationale': 'Preserve the two technologies as columns and compare each using the same criterion and request.',
  'assumptions': 'Illustrative request; rule allowance is not proof of route availability.',
  'units': [
   _unit('comparison', 'Security Group와 NACL — 같은 기준으로 비교', 'Security Group and NACL — same criteria',
     '| 기준 | Security Group | NACL |\n|---|---|---|\n| 적용 범위 | Resource / ENI | Subnet |\n| 연결 상태 추적 (Stateful) | 예 | 아니오 |\n| Allow 규칙 | 지원 | 지원 |\n| Explicit Deny | 미지원 | 지원 |\n\nENI는 리소스의 네트워크 인터페이스다. Stateful은 연결 상태를 추적한다는 뜻이다.',
     '| Criterion | Security Group | NACL |\n|---|---|---|\n| Scope | Resource / ENI | Subnet |\n| Tracks connection state (stateful) | Yes | No |\n| Allow rules | Supported | Supported |\n| Explicit deny | Not supported | Supported |\n\nAn ENI is a resource network interface. Stateful means tracking connection state.'),
   _unit('request', '같은 요청을 두 경계에서 보기', 'One request at two boundaries',
     '**설명용 예시:** 클라이언트 → subnet → 앱 ENI로 가는 동일한 요청을 생각한다. NACL은 subnet 경계, SG는 리소스/ENI 경계의 규칙을 확인하는 비교 대상이다.\n\n명시적 거부 규칙을 찾는다면 NACL 열을 본다. SG에는 Allow 규칙이 있고, 여러 SG를 붙이면 허용 규칙을 합친다. **SG 허용만으로 네트워크 경로가 생기지는 않는다.**',
     '**Illustrative example:** follow the same request from a client → subnet → app ENI. Compare NACL rules at the subnet boundary with SG rules at the resource/ENI boundary.\n\nFor explicit deny rules, look at the NACL column. SGs have allow rules; rules from multiple attached SGs are combined. **An SG allow rule does not create a network route.**'),
   _unit('return-traffic', '응답 트래픽도 같은 예시로 비교', 'Compare return traffic in the same example',
     '클라이언트의 요청을 허용한 뒤 앱이 응답한다고 가정한다. **SG는 연결 상태를 추적하므로 허용된 요청의 응답을 허용한다. NACL은 상태를 추적하지 않아 응답 방향도 규칙으로 허용해야 한다.**\n\nNACL에서 응답 방향을 허용하지 않으면 요청 방향만 허용해도 통신이 완료되지 않을 수 있다. 실제 결과는 경로와 전체 규칙도 확인해야 한다.\n\n[AWS 공식 보충 근거](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)',
     'Assume the client request is allowed and the app sends a response. **An SG tracks connection state and allows the response to an allowed request. A NACL does not track state, so rules must also allow the return direction.**\n\nIf NACL rules do not allow the return direction, permitting only the request may not complete communication. Actual results also depend on routes and the full rule set.\n\n[AWS supplementary source](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)'),
   _unit('references', 'SG 참조가 의미하는 것', 'What an SG reference means',
     'SG 참조는 상대 SG의 규칙을 복사하지 않는다. 연결된 네트워크 인터페이스의 private IP에 적용된다.\n\n따라서 규칙 참조, 허용 규칙 결합, 실제 경로를 따로 확인한다. 표는 이 비교를 설명하며 특정 트래픽의 성공을 보장하지 않는다.\n\n[AWS SG 규칙](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)',
     'An SG reference does not copy the other SG’s rules. It applies to private IPs of associated network interfaces.\n\nCheck rule references, combined allow rules, and the actual route separately. This comparison does not guarantee that a particular request succeeds.\n\n[AWS SG rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)')]},
 ('data-platform-production-operations', '20.3 Incident Drill — Schema Break'): {
  'id': 'schema-break', 'rationale': 'Show the changed contract before tracing impact and response; avoid controls which repeat labels.',
  'assumptions': 'Possible propagation path from the source, not a measured production incident.',
  'units': [
   _unit('change', 'Schema Break — 읽는 계약이 깨질 때', 'Schema break — a broken reading contract',
     '생산자가 필드 이름이나 타입을 바꾸면 소비자가 데이터를 읽지 못할 수 있다. **계약을 깨는 변경인지** 확인하고 영향 구간을 찾는 이유다.\n\n| 변경 전 | 변경 후 |\n|---|---|\n| `amount BIGINT` | `amount STRING` |\n\n소비자가 정수를 기대하는데 문자열을 받는 상황이다. 이 타입 변경이 실제로 호환되는지는 데이터 계약과 소비자 처리를 확인해야 한다.',
     'Changing a field name or type can stop a consumer from reading data. Check whether the change **breaks the contract** and identify the affected range.\n\n| Before | After |\n|---|---|\n| `amount BIGINT` | `amount STRING` |\n\nA consumer expects an integer but receives a string. Check the data contract and consumer behavior to determine actual compatibility.'),
   _unit('propagation', 'Schema Break — 영향이 전달되는 경로', 'Schema break — how impact can propagate',
     '**원문의 가능한 연결 경로:**\n\nProducer → CDC / Event → Flink/Spark → Silver → dbt → Dashboard\n\n앞단의 읽기 실패는 뒤 단계에서 사용할 데이터에 영향을 줄 수 있다. 모든 단계가 반드시 실패한다는 뜻은 아니다. Lineage(데이터 의존 관계)로 어떤 downstream이 영향을 받는지 확인한다.',
     '**Possible chain from the source:**\n\nProducer → CDC / Event → Flink/Spark → Silver → dbt → Dashboard\n\nAn upstream reading failure can affect data used downstream. This does not mean every stage must fail. Use lineage (data dependencies) to identify affected downstream consumers.'),
   _unit('response', 'Schema Break — 대응과 예방', 'Schema break — response and prevention',
     '**대응 순서:** 변경 감지 → 호환되지 않는 데이터 중지/격리 → lineage로 영향 분석 → producer/consumer 수정 → 영향 데이터 backfill → 검증.\n\nBackfill은 영향받은 데이터를 다시 채우는 과정이다. 수정 후 검증까지 필요하다.\n\n**예방:** Data Contracts, Schema Registry, 호환성 검사, CI/CD 검증을 함께 검토한다. Schema Registry라는 이름을 고르는 것만으로 호환성이 확인되지는 않는다.\n\n자동 타입 변환이 업무 의미도 보존하는지 확인한다. 타입·값·건수·downstream 결과를 검증한다. [CDC](cdc-debezium.md), [Lineage](lineage-metadata.md).',
     '**Response order:** detect the change → stop/quarantine incompatible data → analyze impact using lineage → fix producer/consumer → backfill affected data → validate.\n\nBackfill restores the affected data range. Validate after the fix and backfill.\n\n**Prevention:** review data contracts, a schema registry, compatibility checks, and CI/CD validation together. Selecting the name “Schema Registry” does not establish compatibility.\n\nCheck whether automatic type conversion preserves business meaning. Validate types, values, counts and downstream results. See [CDC](cdc-debezium.md) and [lineage](lineage-metadata.md).')]},
}


QLORA_FLOW = {
 'id': 'qlora-flow',
 'rationale': 'Keep every directed source edge visible and connect preparation, training, saved output and evaluation. A static explanation needs no control.',
 'assumptions': 'Illustrative training sample, not an executed run. Supporting sections 4.5–4.14 are bound by the full-document review hash.',
 'units': [
  _unit('prepare', 'QLoRA — 무엇을 준비하고 왜?', 'QLoRA — what to prepare and why?',
   'QLoRA는 **기본 모델(base)을 고정하고 작은 adapter를 학습**해 자원 부담을 낮추는 방식이다. 답변 방식이나 업무 수행 방식을 바꾸려 할 때 검토한다. 모든 문제에 fine-tuning이 필요한 것은 아니다. 자주 바뀌는 정보 검색은 RAG가 더 적합할 수 있다.\n\n**전체 흐름의 시작 — 화살표는 다음 단계로의 진행이다.**\n\n- 문제 정의 → Training Dataset 준비: 원하는 동작을 학습 예제로 만든다.\n- Training Dataset 준비 → Base Model 선택: 데이터와 목표에 맞는 기본 모델을 선택한다.\n- Base Model 선택 → 4-bit Quantization: 기본 모델을 4-bit 형태로 불러 메모리 부담을 낮춘다.\n- 4-bit Quantization → LoRA Adapter 구성: 학습할 작은 adapter와 대상 layer를 정한다.\n\n데이터 형식·loss 범위·저장 조건이 맞아야 원하는 동작을 학습할 수 있다. [원문 4.2–4.6](#42-step-1)',
   'QLoRA **freezes a base model and trains a small adapter** to reduce resource needs. Consider it to change response behavior or task skills. Not every problem requires fine-tuning; RAG may better fit retrieval of changing information.\n\n**Start of the overall flow — arrows mean progression to the next stage.**\n\n- Define the problem → Prepare the Training Dataset: turn the desired behavior into training examples.\n- Prepare the Training Dataset → Select the Base Model: choose a base model suited to the data and goal.\n- Select the Base Model → 4-bit Quantization: load the base in 4-bit form to reduce memory needs.\n- 4-bit Quantization → Configure the LoRA Adapter: choose the small adapter and target layers to train.\n\nData format, loss scope and saving conditions must fit the intended behavior. [Source 4.2–4.6](#42-step-1-define-the-training-goal)'),
  _unit('train', 'QLoRA — 학습에서 실제로 바뀌는 것', 'QLoRA — what actually changes during training',
   '**앞 단계에서 이어짐:** LoRA Adapter 구성 → Training → Validation.\n\nTraining에서는 token 입력으로 다음 token을 예측하고, 지정한 정답 token의 예측으로 loss를 계산한다. loss → gradient → adapter 갱신을 반복한다. Validation에서는 학습 중 성능을 함께 살핀다.\n\n**고정된 base ≠ gradient를 차단한 base.** Base weight는 optimizer가 갱신하지 않지만 frozen base를 통해 gradient가 전달된다. base 연산 전체를 `no_grad`로 감싸는 뜻이 아니다. 4-bit 저장 정밀도와 연산 dtype도 구분한다.\n\n[Tokenization·loss: 4.7](#47-step-5-tokenization) · [갱신: 4.10](#410-step-8-backpropagation)',
   '**Continuing from setup:** Configure the LoRA Adapter → Training → Validation.\n\nTraining predicts the next token from token inputs and computes loss on the selected target tokens. Repeat loss → gradients → adapter updates. Validation checks performance during training as well.\n\n**A frozen base does not block gradients.** The optimizer does not update base weights, but gradients pass through the frozen base. Do not wrap all base operations in `no_grad`. Distinguish 4-bit storage precision from compute dtype.\n\n[Tokenization and loss: 4.7](#47-step-5-tokenization) · [Updates: 4.10](#410-step-8-backpropagation)'),
  _unit('evaluate-save', 'QLoRA — 저장과 승격은 다른 판단', 'QLoRA — saving and promotion are separate decisions',
   '- Validation → Adapter Artifact 저장: 학습 결과인 adapter를 저장한다.\n- Adapter Artifact 저장 → Golden Dataset Evaluation: 저장 이후에도 별도 평가로 업무 성능을 확인한다.\n- Golden Dataset Evaluation → Promote / Reject: 평가 근거로 승격 또는 거부를 판단한다.\n\n**낮은 training loss만으로 승격하지 않는다.** Validation과 실제 업무 평가를 함께 봐야 한다. 위 흐름은 원문의 절차이며, 평가를 수행했거나 품질이 개선됐다는 결과가 아니다.\n\nAdapter 파일에는 base model weight가 없다. 독립된 전체 모델로 생각하면 안 된다. 학습 재개에는 optimizer·scheduler·RNG 같은 상태도 확인한다. [저장 조건: 4.14](#414-training)',
   '- Validation → Save the Adapter Artifact: save the trained adapter.\n- Save the Adapter Artifact → Golden Dataset Evaluation: evaluate task performance separately after saving.\n- Golden Dataset Evaluation → Promote / Reject: use evaluation evidence to decide promotion or rejection.\n\n**Low training loss alone does not justify promotion.** Check validation and real-task evaluation together. This is the source workflow, not evidence that evaluation ran or quality improved.\n\nAdapter files do not contain base model weights and are not a standalone full model. To resume training, also check optimizer, scheduler and RNG state. [Saving conditions: 4.14](#414-save-training-results)'),
  _unit('example', 'QLoRA — 예측 오류가 adapter 갱신으로 이어지는 예', 'QLoRA — from a prediction error to an adapter update',
   '**원문의 설명용 입력:** “Redis와 Kafka의 차이를 설명해줘.” 목표 답변은 Redis는 in-memory data store, Kafka는 event streaming platform이라는 구분이다.\n\n**입력 → 처리:** 모델에 맞는 tokenizer와 chat template으로 token 입력을 만든다. Base + adapter가 다음 token 확률을 예측한다. “둘 다 database”라고 예측했다면 목표 구분을 담지 못한 예다.\n\n**처리 → 결과:** 지정한 정답 token의 예측에서 loss를 계산하고 gradient로 adapter를 갱신한다. 이 loss는 두 문장을 단순 비교한 점수가 아니다. 실제 labels와 mask가 loss 범위를 정한다.\n\n**한계:** 실제 실행 결과나 개선 보장이 아니다. token ID는 tokenizer에 따라 다르며, 한 번 갱신했다고 올바른 답을 보장하지 않는다. 이후 별도 평가가 필요하다. [예제 근거: 4.7–4.10](#47-step-5-tokenization)',
   '**Illustrative input from the source:** “Explain the difference between Redis and Kafka.” The target distinguishes Redis as an in-memory data store and Kafka as an event streaming platform.\n\n**Input → processing:** use the model’s tokenizer and chat template to create token inputs. Base + adapter predict next-token probabilities. A prediction that both are databases misses the intended distinction.\n\n**Processing → result:** compute loss on the selected target tokens, then use gradients to update the adapter. Loss is not a simple score comparing two sentences. Actual labels and masks determine its scope.\n\n**Limits:** this is not an executed result or a guarantee of improvement. Token IDs depend on the tokenizer; one update does not guarantee a correct answer. Separate evaluation is still needed. [Example source: 4.7–4.10](#47-step-5-tokenization)')]
}
DESIGNS[('ai-model-development-qlora-training', '4.1 전체 Training Flow')] = QLORA_FLOW
DESIGNS[('ai-model-development-qlora-training', '4.1 Overall Training Flow')] = QLORA_FLOW


# Hashes bind review to the full selected source span in each language.
SOURCE_HASHES = {('aws-cloud-networking', 'Security Group vs NACL', 'en'): 'b5cebe3ee747a8bdf8cddbe816a8d2a97ac3f62e54c4ed3a6f95905ca5708381',
 ('aws-cloud-networking', 'Security Group vs NACL', 'ko'): 'cc0ee434a73ace665fe38b12686fa67dec98c6de971fe415d8e7aad52407b84e',
 ('data-platform-flink', '5.5 Watermark', 'en'): 'c2a0231e4db08760cbd9106cb63a6b8a575bfe15807b66fe648b6320865d060c',
 ('data-platform-flink', '5.5 Watermark', 'ko'): '0744fb1b1c4c3d323bcdf32af1bf4e0aa1f1d248149ba7326518276dde8ed94f',
 ('data-platform-production-operations', '20.3 Incident Drill — Schema Break', 'en'): '76c3af6dbce1b7fd7ec5f6fd5002257cc1d3278879a451599fc1def5a5c544f2',
 ('data-platform-production-operations', '20.3 Incident Drill — Schema Break', 'ko'): '3b43785bd3a59f9c7e545b29529d7e9109af5278a722ee67c7d0c5b9fab34a30',
 ('english-study-vocabulary', 'vocab-check', 'en'): 'fe61a354b6a3d971b812048bd46843cb27ddbcfde45f07a4f209ab04dd6068a0',
 ('english-study-vocabulary', 'vocab-check', 'ko'): '4fa69b766424d599f2d0750bea359a938e401d9db3979d381584d1db79f205c2',
 ('prompts-flink', 'flink-01', 'en'): '9affe90aa9cba1533440bfe6ee486a842b3e7bc5e484fa5b460cc14c7c468b10',
 ('prompts-flink', 'flink-01', 'ko'): '58cf58551a4e7ffd9fd6d5f1a66bb3ee83a9b58ae9f15dbe529124a6cb3908d8'}


SOURCE_HASHES[('ai-model-development-qlora-training', '4.1 전체 Training Flow', 'ko')] = '8a71f4106eec641165fb9c61f98e88c573f84eea403e32822cf3768fedf9a045'
SOURCE_HASHES[('ai-model-development-qlora-training', '4.1 Overall Training Flow', 'en')] = 'd327f904e67bf951639ed195f7d62c516e1a0f0f48dc73613422559641bf0303'
SUPPORTING_DOCUMENT_HASHES = {('ai-model-development-qlora-training', 'ko'): '11c7af48106bbb0d2d9a46dc16ed8e2df5fc11847464a0725191c272dbe198a4', ('ai-model-development-qlora-training', 'en'): '0c24a4ed7a7877601e8f075c72ba576cd5f89f27136ecbf6dc9a3ec2ef9d51a9'}

def _window_prompt_units(original, language):
    """The reviewed prompt is natural-language prose, not executable code.

    Preserve each original instruction verbatim in a meaningful, readable unit.
    Parse the full Markdown structure rather than guessing text after a fence.
    """
    import html
    import markdown
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(markdown.markdown(original, extensions=[
        'pymdownx.superfences', 'pymdownx.tabbed', 'attr_list']), 'html.parser')
    tabset = soup.select_one('.tabbed-set')
    if tabset is None:
        return None
    labels = tabset.find_all('label', recursive=False)
    contents = tabset.find_all('div', class_='tabbed-content', recursive=False)
    if len(labels) != 2 or len(contents) != 2:
        return None
    groups = [('context', '상황과 비교 요청', 'Context and comparison request', slice(0, 2)),
              ('contract', '판단 조건과 기대 출력', 'Conditions and expected output', slice(2, 5))]
    units = []
    for label, content in zip(labels, contents):
        prompt_language = 'en' if label.get_text(strip=True) == 'English' else 'ko'
        code = content.find('code')
        lines = code.get_text().strip().splitlines() if code else []
        if len(lines) != 5:
            return None
        for key, ko_title, en_title, span in groups:
            title = (ko_title if language == 'ko' else en_title) + ' · ' + ('English' if prompt_language == 'en' else '한국어')
            units.append({'key': 'request-' + prompt_language + '-' + key,
                          'title': title,
                          'body': ''.join('<blockquote><p>' + html.escape(line) + '</p></blockquote>' for line in lines[span])})
    tabset.decompose()
    guidance = soup.find_all('p')
    if guidance:
        units.append({'key': 'guidance',
                      'title': '요청을 해석할 때 주의할 점' if language == 'ko' else 'How to interpret the request',
                      'body': ''.join(str(p) for p in guidance)})
    return units


def reviewed_design(document_id, heading, anchor, language, original, *, full_source=None):
    """Return a bounded design or None; source form alone never selects an interaction."""
    import hashlib
    supporting_hash = SUPPORTING_DOCUMENT_HASHES.get((document_id, language))
    if supporting_hash and (full_source is None or hashlib.sha256(full_source.encode()).hexdigest() != supporting_hash):
        return None
    expected = SOURCE_HASHES.get((document_id, anchor or heading, language))
    if not expected or hashlib.sha256(original.encode()).hexdigest() != expected:
        return None
    design = DESIGNS.get((document_id, heading))
    if design:
        return {**design, 'units': [{'key': u['key'], 'title': u['title'][language],
                                    'body': u['body'][language]} for u in design['units']]}
    if document_id == 'english-study-vocabulary' and anchor == 'vocab-check':
        return {'id': anchor, 'rationale': 'Meaning, usage and bilingual example remain visible together.',
                'assumptions': 'Neutral workplace usage; corpus counts describe only this handbook.',
                'units': [{'key': 'meaning-usage', 'title': 'check', 'body': original}]}
    if document_id == 'prompts-flink' and anchor == 'flink-01':
        context = ('**용도:** 지표 정의에 맞는 window를 비교하는 검토 요청이다.\n\n**필요한 입력:** 업무 지표의 구간 경계, 실제 SQL·설정, 표본 이벤트와 늦은 이벤트 허용 규칙.\n\n**기대 출력의 형태 (설명용):** 각 표본 → 소속 window → 기대 결과 → 늦은 이벤트 처리 질문. 구간과 표본을 받기 전에는 실제 소속을 단정하지 않는다.' if language == 'ko' else
                   '**Purpose:** request a review comparing windows against metric definitions.\n\n**Required input:** business window boundaries, actual SQL/settings, sample events, and late-event rules.\n\n**Expected output shape (illustrative):** each sample → window membership → expected result → late-event policy questions. Do not assert actual membership before receiving boundaries and samples.')
        prompt_units = _window_prompt_units(original, language)
        if prompt_units is None:
            return None
        worked_example = ('**설명용 가정:** event-time 구간 `[10:00, 10:01)`은 시작을 포함하고 끝을 제외한다. 원문의 겹치지 않는 tumbling window 예시를 사용한다.\n\n**입력 → 결과:** 이벤트 시각 `10:00:20` → 첫 구간에 속함 → 그 구간의 이벤트 건수 `+1`. 시각이 두 경계 사이에 있기 때문이다.\n\n실제 모델 실행이나 트래픽 결과가 아니다. 늦은 이벤트의 반영·결과 확정은 watermark와 정책을 별도로 확인한다. [Window 원문](../data-platform/flink.md#tumbling-window)' if language == 'ko' else
                          '**Illustrative assumption:** event-time interval `[10:00, 10:01)` includes its start and excludes its end. This uses the source’s non-overlapping tumbling-window example.\n\n**Input → result:** event time `10:00:20` → belongs to the first interval → event count for that interval `+1`, because the time is within its bounds.\n\nThis is not an actual model run or traffic result. Late-event inclusion and finalization still depend on the watermark and policy. [Window source](../data-platform/flink.md#tumbling-window)')
        return {'id': anchor, 'rationale': 'Explain intent and evidence, then preserve every request sentence in a meaningful prose unit. The original provides the unbroken copyable prompt.',
                'assumptions': 'Review only; no actual input or model output is claimed.',
                'units': [{'key': 'purpose-input-output', 'title': heading, 'body': context},
                          {'key': 'worked-example', 'title': '기대 출력 예시 — 구간 소속' if language == 'ko' else 'Expected output example — window membership', 'body': worked_example}] + prompt_units}
    return None
