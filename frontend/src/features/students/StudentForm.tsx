/**
 * Student Form Component
 */
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { studentsService } from '@/services'
import { Student } from '@/types'

const studentSchema = z.object({
  reg_no: z.string().min(1, 'Registration number is required'),
  name: z.string().min(1, 'Name is required'),
  program: z.string().min(1, 'Program is required'),
  status: z.enum(['Active', 'Inactive', 'Graduated', 'Suspended']),
})

type StudentFormData = z.infer<typeof studentSchema>

interface StudentFormProps {
  student?: Student | null
  onClose: () => void
  onSuccess: () => void
}

export function StudentForm({ student, onClose, onSuccess }: StudentFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<StudentFormData>({
    resolver: zodResolver(studentSchema),
    defaultValues: student || {
      reg_no: '',
      name: '',
      program: '',
      status: 'Active',
    },
  })

  const mutation = useMutation({
    mutationFn: (data: StudentFormData) =>
      student
        ? studentsService.update(student.id, data)
        : studentsService.create(data),
    onSuccess: () => {
      toast.success(student ? 'Student updated successfully' : 'Student created successfully')
      onSuccess()
    },
    onError: () => {
      toast.error('Failed to save student')
    },
  })

  const onSubmit = (data: StudentFormData) => {
    mutation.mutate(data)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">
          {student ? 'Edit Student' : 'Add Student'}
        </h2>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Registration Number</label>
            <Input {...register('reg_no')} error={errors.reg_no?.message} />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <Input {...register('name')} error={errors.name?.message} />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Program</label>
            <Input {...register('program')} error={errors.program?.message} />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              {...register('status')}
              className="w-full px-4 py-3 rounded-2xl border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
              <option value="Graduated">Graduated</option>
              <option value="Suspended">Suspended</option>
            </select>
            {errors.status && (
              <p className="mt-1 text-sm text-red-600">{errors.status.message}</p>
            )}
          </div>

          <div className="flex justify-end space-x-2 pt-4">
            <Button type="button" variant="ghost" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? 'Saving...' : 'Save'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
