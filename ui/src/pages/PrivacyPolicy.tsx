import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowLeft, Shield } from 'lucide-react'

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-bg py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <Link
            to="/login"
            className="inline-flex items-center text-primary hover:text-primary-hover transition-colors mb-6"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Login
          </Link>
          
          <div className="flex items-center space-x-4 mb-4">
            <div className="p-3 bg-primary/10 rounded-xl">
              <Shield className="w-8 h-8 text-primary" />
            </div>
            <div>
              <h1 className="text-3xl sm:text-4xl font-bold text-text-primary">
                Privacy Policy
              </h1>
              <p className="text-text-muted mt-1">
                Last updated: December 4, 2025
              </p>
            </div>
          </div>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card space-y-8"
        >
          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              1. Introduction
            </h2>
            <p className="text-text-secondary leading-relaxed">
              Agentic Workflows ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our Service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              2. Information We Collect
            </h2>
            
            <h3 className="text-xl font-semibold text-text-primary mb-3 mt-6">
              2.1 Personal Information
            </h3>
            <p className="text-text-secondary leading-relaxed mb-4">
              We collect information that you provide directly to us, including:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Name and email address</li>
              <li>Company name and role</li>
              <li>Account credentials</li>
              <li>Payment information</li>
              <li>Profile information</li>
            </ul>

            <h3 className="text-xl font-semibold text-text-primary mb-3 mt-6">
              2.2 Usage Information
            </h3>
            <p className="text-text-secondary leading-relaxed mb-4">
              We automatically collect certain information about your device and how you interact with our Service:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Log data (IP address, browser type, pages visited)</li>
              <li>Device information (operating system, device identifiers)</li>
              <li>Usage patterns and preferences</li>
              <li>Workflow execution data</li>
              <li>Performance metrics</li>
            </ul>

            <h3 className="text-xl font-semibold text-text-primary mb-3 mt-6">
              2.3 Cookies and Tracking Technologies
            </h3>
            <p className="text-text-secondary leading-relaxed">
              We use cookies and similar tracking technologies to track activity on our Service and store certain information. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              3. How We Use Your Information
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              We use the collected information for various purposes:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Provide, maintain, and improve our Service</li>
              <li>Process transactions and send related information</li>
              <li>Send technical notices and support messages</li>
              <li>Respond to your comments and questions</li>
              <li>Monitor and analyze trends and usage</li>
              <li>Detect, prevent, and address technical issues</li>
              <li>Personalize your experience</li>
              <li>Send marketing communications (with your consent)</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              4. Data Sharing and Disclosure
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              We may share your information in the following situations:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li><strong>Service Providers:</strong> With third-party vendors who perform services on our behalf</li>
              <li><strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets</li>
              <li><strong>Legal Requirements:</strong> When required by law or to protect our rights</li>
              <li><strong>With Your Consent:</strong> When you explicitly agree to share your information</li>
            </ul>
            <p className="text-text-secondary leading-relaxed mt-4">
              We do not sell your personal information to third parties.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              5. Data Security
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              We implement appropriate technical and organizational measures to protect your personal information:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Encryption of data in transit and at rest</li>
              <li>Regular security assessments and audits</li>
              <li>Access controls and authentication</li>
              <li>Secure data centers and infrastructure</li>
              <li>Employee training on data protection</li>
            </ul>
            <p className="text-text-secondary leading-relaxed mt-4">
              However, no method of transmission over the Internet is 100% secure, and we cannot guarantee absolute security.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              6. Data Retention
            </h2>
            <p className="text-text-secondary leading-relaxed">
              We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required by law. When we no longer need your information, we will securely delete or anonymize it.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              7. Your Rights
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              Depending on your location, you may have the following rights:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li><strong>Access:</strong> Request a copy of your personal information</li>
              <li><strong>Correction:</strong> Request correction of inaccurate information</li>
              <li><strong>Deletion:</strong> Request deletion of your personal information</li>
              <li><strong>Portability:</strong> Request transfer of your data to another service</li>
              <li><strong>Objection:</strong> Object to processing of your information</li>
              <li><strong>Restriction:</strong> Request restriction of processing</li>
              <li><strong>Withdraw Consent:</strong> Withdraw consent at any time</li>
            </ul>
            <p className="text-text-secondary leading-relaxed mt-4">
              To exercise these rights, please contact us at privacy@agenticworkflows.com
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              8. International Data Transfers
            </h2>
            <p className="text-text-secondary leading-relaxed">
              Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place to protect your information in accordance with this Privacy Policy and applicable laws.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              9. Children's Privacy
            </h2>
            <p className="text-text-secondary leading-relaxed">
              Our Service is not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If you become aware that a child has provided us with personal information, please contact us.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              10. Changes to This Privacy Policy
            </h2>
            <p className="text-text-secondary leading-relaxed">
              We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date. We encourage you to review this Privacy Policy periodically.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              11. Contact Us
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              If you have any questions about this Privacy Policy, please contact us:
            </p>
            <div className="p-4 bg-bg-secondary rounded-lg space-y-2">
              <p className="text-text-primary font-medium">Agentic Workflows</p>
              <p className="text-text-secondary">Email: privacy@agenticworkflows.com</p>
              <p className="text-text-secondary">Support: support@agenticworkflows.com</p>
              <p className="text-text-secondary">Data Protection Officer: dpo@agenticworkflows.com</p>
            </div>
          </section>

          <section className="border-t-2 border-border pt-6">
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              12. GDPR Compliance
            </h2>
            <p className="text-text-secondary leading-relaxed">
              For users in the European Economic Area (EEA), we comply with the General Data Protection Regulation (GDPR). Our lawful basis for processing your data includes consent, contract performance, legal obligations, and legitimate interests.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              13. CCPA Compliance
            </h2>
            <p className="text-text-secondary leading-relaxed">
              For California residents, we comply with the California Consumer Privacy Act (CCPA). You have the right to know what personal information we collect, delete your information, and opt-out of the sale of your information (which we do not do).
            </p>
          </section>
        </motion.div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mt-8 text-center"
        >
          <p className="text-text-muted text-sm">
            By using Agentic Workflows, you agree to our{' '}
            <Link to="/terms-of-service" className="text-primary hover:text-primary-hover">
              Terms of Service
            </Link>
            {' '}and this Privacy Policy
          </p>
        </motion.div>
      </div>
    </div>
  )
}
