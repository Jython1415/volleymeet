import React from 'react';

const AttachmentList = ({ attachments }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Attachment Id</th>
                    <th>Meeting Id</th>
                    <th>Attachment Url</th>
                </tr>
            </thead>
            <tbody>
                {attachments.map((attachment) => (
                    <tr key={attachment.attachment_id} style={{ marginBottom: '20px' }}>
                        <td>{attachment.attachment_id}</td>
                        <td>{attachment.meeting_id}</td>
                        <td>{attachment.attachment_url}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default AttachmentList;