import React, { useState } from 'react';
import './FAQ.css';

const FAQ = () => {
  const [activeIndex, setActiveIndex] = useState(null);

  const toggleFAQ = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  const faqs = [
    {
      question: 'What is Uniguide?',
      answer: 'Uniguide is a comprehensive student assistance platform specifically designed for students at Notre Dame University-Louaize (NDU) in Lebanon. It helps with scheduling courses, answering university-related questions, preparing for exams, and providing access to notes taken by fellow students.',
    },
    {
      question: 'What are the main features of Uniguide?',
      answer: 'Uniguide has two main modes: Uniguide Advisor and Exam Pal. It also includes a notes page for accessing notes shared by other students at NDU.',
    },
    {
      question: 'What does the Uniguide Advisor do?',
      answer: 'The Uniguide Advisor assists NDU students by scheduling their courses and answering questions related to their university experience.',
    },
    {
      question: 'How can I use the Uniguide Advisor to schedule my courses?',
      answer: 'You can input your course preferences and requirements, and the Uniguide Advisor will generate an optimal schedule for you.',
    },
    {
      question: 'Can the Uniguide Advisor answer specific questions about Notre Dame University-Louaize?',
      answer: 'Yes, the Uniguide Advisor is trained to provide answers to a wide range of questions specific to NDU, including course requirements and more.',
    },
    {
      question: 'What is Exam Pal?',
      answer: 'Exam Pal is a feature of Uniguide that helps NDU students prepare for their exams by analyzing documents and files related to their study material.',
    },
    {
      question: 'How does Exam Pal help with exam preparation?',
      answer: 'Exam Pal processes your study materials, highlights key concepts, suggests important topics, and provides summaries to help you study more efficiently.',
    },
    {
      question: 'Can I upload my own documents to Exam Pal?',
      answer: 'Yes, NDU students are encouraged to share their notes to help their peers. You can send your notes to us at notes@uniguide.com so we can check them to maintain credibility with our notes before uploading them.',
    },
    {
      question: 'What is the Notes Page?',
      answer: 'The Notes Page is a section of Uniguide where NDU students can download notes taken by fellow students for various courses.',
    },
    {
      question: 'How can I access notes on the Notes Page?',
      answer: 'You can browse through the available notes for your courses and read them to help with your studies.',
    },
    {
      question: 'Can I share my own notes on the Notes Page?',
      answer: 'Yes, NDU students are encouraged to share their notes to help their peers. You can upload your notes to the platform for others to access.',
    },

    {
      question: 'Who do I contact for technical support?',
      answer: 'For technical support, please visit our contact us page on the website and our team is always there for you.',
    },
    
  ];
  
  return (
    <div className="faq-container">
      <h2 className="faq-heading">Frequently Asked Questions</h2>
      {faqs.map((faq, index) => (
        <div className="faq-item" key={index}>
          <h3 className="faq-question" onClick={() => toggleFAQ(index)}>
            {faq.question}
          </h3>
          <div className={`faq-answer ${activeIndex === index ? 'active' : ''}`}>
            <p>{faq.answer}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default FAQ;
