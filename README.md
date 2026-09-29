# Substation by K

## Operational Intelligence for Digital Substations

> **"From communication to diagnosis."**

The operational intelligence platform that transforms automation, protection, and communication data into **diagnosis, history, evidence, and action recommendations** for digital substations.

---

## Overview

**Substation by K** is not just another IEC 61850 protocol analyzer. It is an **operational intelligence platform** that understands substation context, identifies patterns, diagnoses problems, and provides evidence-based recommendations.

### Value Proposition

| What the market offers | What we offer |
|------------------------|----------------|
| Packet visualization | **Diagnosis with evidence** |
| Protocol analysis | **Operational intelligence** |
| Testing tools | **Substation historical memory** |
| Isolated monitoring | **Digital Twin + Predictive analysis** |

---

## Business Plan

### 1. Business Model

#### Products

| Product | Target Audience | Commercial Model | Features |
|---------|-----------------|------------------|----------|
| **K-Integrator** | Integrators, O&M | Subscription + Projects | Diagnosis, commissioning, reports |
| **K-Utility** | Utilities | Annual subscription per substation | Continuous monitoring, Digital Twin, history |
| **K-Lab** | Manufacturers, laboratories | Corporate license | Testing, simulation, validation |

#### Pricing (Initial Estimate)

- **K-Integrator**: BRL 20,000 - BRL 50,000/year + BRL 5,000 - BRL 15,000 per project
- **K-Utility**: BRL 15,000 - BRL 30,000/substation/year
- **K-Lab**: BRL 100,000 - BRL 250,000/year (corporate)

### 2. Market Strategy

#### Launch Phases

```
Phase 1 (0-12 months): K-Integrator
├── MVP: K-Diagnosis + K-Reports
├── Customers: 5-10 integrators
├── Substations: 20-50
└── Revenue: BRL 500K - BRL 1M

Phase 2 (12-24 months): K-Utility
├── Full version: 5 modules
├── Customers: 3-5 utilities
├── Substations: 50-100
└── Revenue: BRL 1M - BRL 3M

Phase 3 (24-36 months): K-Lab + Expansion
├── Corporate product
├── Customers: Global manufacturers
├── Substations: 100+
└── Revenue: BRL 3M - BRL 10M
```

#### Sales Channels

1. **Direct Sales**: Sales team for large customers
2. **Partnerships**: Collaboration with IED manufacturers
3. **Distribution**: Integrators as resellers
4. **Digital**: Website, webinars, whitepapers

### 3. Initial Costs

| Item | Cost (BRL) | Period |
|------|------------|--------|
| MVP development | 200,000 | 6 months |
| Technical team (3 devs) | 30,000/month | Ongoing |
| Cloud infrastructure | 5,000/month | Ongoing |
| Marketing | 15,000/month | Ongoing |
| Sales | 20,000/month | Ongoing |
| **Total Year 1** | **500,000** | - |

### 4. Revenue Projection (3 years)

| Year | Customers | Substations | Revenue (BRL) | Profit (BRL) |
|------|-----------|-------------|---------------|--------------|
| 1 | 10 | 30 | 1,500,000 | -200,000 |
| 2 | 25 | 80 | 4,000,000 | 1,200,000 |
| 3 | 50 | 150 | 8,000,000 | 3,500,000 |

---

## Product Architecture

### Main Modules

```
┌─────────────────────────────────────────────────────────────┐
│                    SUBSTATION BY K                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ K-Discover  │  │K-Digital Twin│  │      K-Diagnosis    │  │
│  │   (v1.1)    │  │    (v1.2)    │  │       (v1.0)        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  K-Guardian │  │  K-Reports  │  │       K-AI          │  │
│  │   (v1.3)    │  │    (v1.0)   │  │      (v2.0)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### MVP (v1.0)

**Initial Modules:**
- K-Diagnosis (core of the product)
- K-Reports (report generator)

**MVP Features:**
1. Import SCD/CID/ICD
2. Capture/analyze network traffic
3. Map signal paths
4. Generate diagnosis + report

### Version Roadmap

| Version | Modules | Target | Status |
|---------|---------|--------|--------|
| v1.0 | K-Diagnosis, K-Reports | Q1 2025 | In development |
| v1.1 | +K-Discover | Q2 2025 | Planned |
| v1.2 | +K-Digital Twin | Q3 2025 | Planned |
| v1.3 | +K-Guardian | Q4 2025 | Planned |
| v2.0 | +K-AI, Substation Memory™ | Q2 2026 | Planned |

---

## Detailed Modules

### 1. K-Discover (Automatic Discovery)

**Objective:** Automatically map the entire substation topology.

**Features:**
- Discovery of IEDs, switches, gateways, RTUs, SCADA
- Protocol identification: GOOSE, MMS, Sampled Values, IEC-104, DNP3, SNMP, PTP, PRP
- Mapping of IPs, MACs, VLANs
- Synchronism verification
- Live substation map generation

**Technologies:**
- Network scanning (ARP, ICMP, SNMP)
- Protocol parsing (libiec61850, libpcap)
- Topology inference algorithms

### 2. K-Digital Twin

**Objective:** Maintain an accurate digital representation of the expected vs. actual architecture.

**Features:**
- Import SCD/CID/ICD
- Comparison: Design vs. Configuration vs. Actual network
- Divergence detection
- 3D/interactive visualization
- Scenario simulation

**Differentiator:** Substation Memory™ - Complete change history

### 3. K-Diagnosis (Intelligent Diagnosis)

**Objective:** Answer: What happened? Where? Why?

**Features:**
- Signal path tracing
- Identification of failure points
- Probability of causes
- Evidence for each hypothesis
- Action recommendations

**Example Output:**
```
Event: SCADA lost position of circuit breaker Q01

Diagnosis:
├── Probability of gateway failure: 85%
│   └── Evidence:
│       ├── IED continues publishing state
│       ├── GOOSE is present
│       ├── Switch records traffic
│       ├── IED→gateway communication active
│       ├── Point not observed in IEC-104
│       └── Last configuration: gateway (2024-11-15)
└── Next steps:
    1. Verify IEC-104 mapping on the gateway
    2. Check gateway logs
    3. Test connectivity with SCADA
```

### 4. K-Guardian (Governance and Integrity)

**Objective:** Monitor changes and ensure configuration integrity.

**Features:**
- Substation baseline (approved state)
- Real-time change detection
- Change logging (when, where, what, impact)
- Non-compliance alerts
- Version history

### 5. K-Reports (Automatic Reports)

**Objective:** Eliminate hours of manual documentation work.

**Report Types:**
- **FAT**: Factory acceptance test report
- **SAT**: Commissioning report
- **O&M**: Substation health report
- **Incident**: Problem analysis
- **Audit**: Change history
- **Engineering**: Design vs. actual comparison

### 6. K-AI (Artificial Intelligence)

**Objective:** Evidence-assisted diagnosis.

**Features:**
- Historical event analysis
- Pattern identification
- Hypothesis generation with evidence
- Recommendations based on previous cases
- Substation Memory™: Substation knowledge base

**Differentiator:** The AI **explains** its conclusions with concrete data.

---

## Competitive Differentiators

### 1. Substation Memory™

**What it is:** Historical knowledge base of the substation.

**Benefits:**
- Learns from past problems
- Identifies recurring patterns
- Provides solutions that worked before
- Creates a digital "institutional memory"

### 2. Manufacturer Agnosticism

**Support for:**
- SEL, Siemens, Schneider, GE, ABB, WEG, and others
- IEC 61850, IEC-104, DNP3, Modbus, SNMP, PTP, PRP

**Advantage:** Does not compete with manufacturers; it **complements** their systems.

### 3. Hybrid Architecture (Edge + Cloud)

```
┌─────────────────────────────────────────────────────────────┐
│                        CLOUD                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   K-AI          │  │  K-Reports      │  │  Dashboard  │  │
│  │  (Analysis)     │  │  (Generation)   │  │(Visualization)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                       EDGE (At substation)                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ K-Discover      │  │ K-Diagnosis     │  │ K-Guardian  │  │
│  │ K-Digital Twin  │  │ (Processing)    │  │ (Monitoring)│  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    OT NETWORK (Real Time)                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │
│  │  IEDs   │  │ Switches│  │ Gateways│  │   SCADA     │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Advantages:**
- Sensitive processing remains on the OT network (security)
- Low latency for real-time diagnosis
- Cloud scalability

### 4. Evidence-Based Approach

**We do not say:** "The problem is the gateway"

**We say:** "The problem is probably the gateway because:
1. The IED is publishing the signal correctly (evidence: GOOSE packets)
2. The switch records traffic to the gateway (evidence: SNMP logs)
3. The gateway does not forward to SCADA (evidence: absence in IEC-104)
4. The last configuration was on the gateway (evidence: change history)"

---

## Technologies and Implementation

### Backpropagation and Feedforward for Data Processing

The system uses **backpropagation** and **feedforward** techniques to:

1. **Backpropagation (Failure Analysis):**
   - Trace the reverse path of failed signals
   - Identify breakpoints in the communication chain
   - Calculate probabilities of causes

2. **Feedforward (Optimization):**
   - Predict impacts of configuration changes
   - Simulate scenarios before implementation
   - Optimize communication routes

### Data Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA FLOW                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Data Capture → Processing → Analysis → Diagnosis           │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Network    │    │  Backprop   │    │  Feedforward│      │
│  │  Sniffer    │───▶│  Engine     │───▶│  Engine     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                       │                                     │
│                       ▼                                     │
│                  ┌─────────────┐                            │
│                  │  Knowledge  │                            │
│                  │  Graph      │                            │
│                  └─────────────┘                            │
│                       │                                     │
│                       ▼                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                SUBSTATION MEMORY™                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Capture** | libpcap, Wireshark, tshark |
| **Protocols** | libiec61850, libdnp3, libmodbus |
| **Processing** | Python, C++, Rust |
| **Backpropagation** | TensorFlow/PyTorch (for pattern analysis) |
| **Feedforward** | Graph algorithms, simulation engines |
| **Storage** | PostgreSQL, TimescaleDB, Elasticsearch |
| **Visualization** | React, D3.js, Three.js |
| **Edge** | Docker, Kubernetes (Edge), Raspberry Pi/Industrial PCs |
| **Cloud** | AWS/Azure/GCP, Kubernetes |

---

## Success Metrics

### For the Customer

- **Diagnosis time reduction**: 70-90%
- **Savings in engineering hours**: 50-70%
- **Availability increase**: 1-3%
- **Report generation time**: 90% faster

### For the Business

- **MVP conversion rate**: 20-30%
- **Average ticket**: BRL 20,000 - BRL 50,000/year per substation
- **Annual growth**: 100-200%
- **NPS (Net Promoter Score)**: 50+

---

## Market and Competition

### Competitive Analysis

| Competitor | Product | Strengths | Weaknesses | Our Differentiator |
|------------|---------|-----------|------------|--------------------|
| OMICRON | StationScout | Comprehensive view, diagnosis | Focus on testing, not operational intelligence | **Intelligence + History + Evidence** |
| Conprove | SV/GOOSE Monitor | Local monitoring, good for SV | Limited to specific protocols | **Multi-protocol + Digital Twin + AI** |
| Siemens | SICAM | Integration with their equipment | Proprietary, limited to their ecosystem | **Agnostic + Substation Memory™** |
| SEL | SEL-5030 | Protocol analysis | Focused on their own IEDs | **Manufacturer-independent** |

### Entry Barriers

1. **Specialized knowledge**: IEC 61850 and automation systems
2. **Installed base**: Customers already use existing solutions
3. **Certifications**: Requirements for critical systems

### Our Advantages

1. **Unique focus**: Operational intelligence, not just monitoring
2. **Agnosticism**: Works with any manufacturer
3. **Substation Memory™**: Unique competitive barrier
4. **Flexible business model**: Adapts to different customers

---

## Launch Strategy

### Immediate Steps

1. **Finalize MVP (3 months)**
   - K-Diagnosis (signal path analysis)
   - K-Reports (basic report generation)
   - Simple web interface

2. **Tests with Early Adopters (2 months)**
   - 3-5 partner integrators
   - 10-20 pilot substations
   - Feedback and adjustments

3. **Official Launch (Month 6)**
   - Website and marketing materials
   - Webinars and whitepapers
   - Partnerships with manufacturers

### Ideal Customers for MVP

1. **Automation integrators** (Priority 1)
   - Feel the pain of fast diagnosis
   - Can use it in multiple projects
   - Shorter sales cycle

2. **O&M companies** (Priority 2)
   - Need for continuous monitoring
   - Value history and reports

3. **Innovative utilities** (Priority 3)
   - Willing to test new technologies
   - Have multiple substations

---

## Next Steps

### Short Term (1-3 months)

- [x] Define MVP scope
- [x] Create Business Plan
- [ ] Develop K-Diagnosis (core)
- [ ] Implement backpropagation for failure analysis
- [ ] Create report generator (K-Reports)
- [ ] Test with real substation data

### Medium Term (3-6 months)

- [ ] Launch MVP for early adopters
- [ ] Develop K-Discover
- [ ] Implement basic Digital Twin
- [ ] Create visualization dashboards
- [ ] Establish first partnerships

### Long Term (6-12 months)

- [ ] Launch full version (v1.3)
- [ ] Add K-AI and Substation Memory™
- [ ] Expand to international market
- [ ] Create certification program

---

## Contact

For more information about **Substation by K**:

- **Website**: [substationbyk.com](https://substationbyk.com) (under development)
- **Email**: contact@substationbyk.com
- **LinkedIn**: [Substation by K](https://linkedin.com/company/substationbyk)

---

## Additional Documentation

- [Detailed Technical Plan](docs/technical/technical_plan.md)
- [System Architecture](docs/architecture/system_architecture.md)
- [Module Specifications](docs/modules/)
- [Marketing Strategy](docs/business/marketing_strategy.md)
- [Financial Model](docs/business/financial_model.md)

---

> **"Transforming data into operational intelligence for digital substations."**

*Substation by K - v1.0 | Business Plan | Last updated: November 2024*
