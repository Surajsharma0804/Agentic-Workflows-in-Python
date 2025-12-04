import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowLeft, FileText } from 'lucide-react'

export default function TermsOfService() {
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
              <FileText className="w-8 h-8 text-primary" />
            </div>
            <div>
              <h1 className="text-3xl sm:text-4xl font-bold text-text-primary">
                Terms of Service
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
              1. Acceptance of Terms
            </h2>
            <p className="text-text-secondary leading-relaxed">
              By accessing and using Agentic Workflows ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to these Terms of Service, please do not use the Service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              2. Description of Service
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              Agentic Workflows provides an AI-powered workflow automation platform that enables users to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Create and manage automated workflows</li>
              <li>Integrate with various AI models and services</li>
              <li>Execute tasks and processes automatically</li>
              <li>Monitor and audit workflow executions</li>
              <li>Collaborate with team members</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              3. User Accounts
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              To use certain features of the Service, you must register for an account. You agree to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Provide accurate, current, and complete information</li>
              <li>Maintain the security of your password</li>
              <li>Accept responsibility for all activities under your account</li>
              <li>Notify us immediately of any unauthorized use</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              4. Acceptable Use
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              You agree not to use the Service to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Violate any laws or regulations</li>
              <li>Infringe on intellectual property rights</li>
              <li>Transmit malicious code or viruses</li>
              <li>Attempt to gain unauthorized access to systems</li>
              <li>Interfere with or disrupt the Service</li>
              <li>Use the Service for any illegal or unauthorized purpose</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              5. Intellectual Property
            </h2>
            <p className="text-text-secondary leading-relaxed">
              The Service and its original content, features, and functionality are owned by Agentic Workflows and are protected by international copyright, trademark, patent, trade secret, and other intellectual property laws.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              6. User Content
            </h2>
            <p className="text-text-secondary leading-relaxed mb-4">
              You retain all rights to the content you create using the Service. By using the Service, you grant us a license to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-text-secondary ml-4">
              <li>Store and process your content to provide the Service</li>
              <li>Create backups and ensure data redundancy</li>
              <li>Analyze usage patterns to improve the Service</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              7. Payment and Billing
            </h2>
            <p className="text-text-secondary leading-relaxed">
              Some features of the Service may require payment. You agree to provide accurate billing information and authorize us to charge your payment method for all fees incurred. Subscription fees are non-refundable except as required by law.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              8. Termination
            </h2>
            <p className="text-text-secondary leading-relaxed">
              We may terminate or suspend your account and access to the Service immediately, without prior notice, for any reason, including breach of these Terms. Upon termination, your right to use the Service will immediately cease.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              9. Disclaimer of Warranties
            </h2>
            <p className="text-text-secondary leading-relaxed">
              THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. WE DO NOT WARRANT THAT THE SERVICE WILL BE UNINTERRUPTED, SECURE, OR ERROR-FREE.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              10. Limitation of Liability
            </h2>
            <p className="text-text-secondary leading-relaxed">
              IN NO EVENT SHALL AGENTIC WORKFLOWS BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING OUT OF OR RELATED TO YOUR USE OF THE SERVICE.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              11. Changes to Terms
            </h2>
            <p className="text-text-secondary leading-relaxed">
              We reserve the right to modify these Terms at any time. We will notify users of any material changes via email or through the Service. Your continued use of the Service after such modifications constitutes acceptance of the updated Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              12. Contact Information
            </h2>
            <p className="text-text-secondary leading-relaxed">
              If you have any questions about these Terms, please contact us at:
            </p>
            <div className="mt-4 p-4 bg-bg-secondary rounded-lg">
              <p className="text-text-primary font-medium">Agentic Workflows</p>
              <p className="text-text-secondary">Email: legal@agenticworkflows.com</p>
              <p className="text-text-secondary">Support: support@agenticworkflows.com</p>
            </div>
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
            By using Agentic Workflows, you agree to these Terms of Service and our{' '}
            <Link to="/privacy-policy" className="text-primary hover:text-primary-hover">
              Privacy Policy
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  )
}
