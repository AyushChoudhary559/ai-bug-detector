package com.cs.bugdetector.repository;

import com.cs.bugdetector.entity.AuditRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface AuditRecordRepository extends JpaRepository<AuditRecord, Long> {
    List<AuditRecord> findByUserIdOrderByCreatedAtDesc(Long userId);
    long countByUserId(Long userId);
}
