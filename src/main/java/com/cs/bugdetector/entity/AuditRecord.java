package com.cs.bugdetector.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "audit_records")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AuditRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = true)
    private User user;

    private String language;
    private String fileName;
    
    @Column(columnDefinition = "TEXT")
    private String code;
    
    private Integer score;
    private String status;
    private Integer bugsCount;
    private Integer securityCount;
    private String timeComplexity;
    private String spaceComplexity;
    
    @Column(columnDefinition = "LONGTEXT")
    private String rawResultJson;

    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        if (this.createdAt == null) {
            this.createdAt = LocalDateTime.now();
        }
    }
}